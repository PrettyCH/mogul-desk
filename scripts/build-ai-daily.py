#!/usr/bin/env python3
"""Build pages/ai-daily.html from data/aihot-daily.json (or a path arg).

Routine jobs should: curl AIHOT daily API → overwrite data/aihot-daily.json → run this script.
Does not fetch the network itself.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "data" / "aihot-daily.json"
OUT_HTML = ROOT / "pages" / "ai-daily.html"
SHANGHAI = timezone(timedelta(hours=8))

SECTION_SHORT = {
    "模型发布/更新": "模型",
    "产品发布/更新": "产品",
    "行业动态": "行业",
    "论文研究": "研究",
    "技术与观点": "技术",
    "快讯": "快讯",
}


def esc(s: object) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def to_shanghai(iso: str | None) -> str | None:
    if not iso:
        return None
    try:
        raw = iso.replace("Z", "+00:00")
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(SHANGHAI).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return None


def primary_link(links: dict | None) -> tuple[str | None, str | None]:
    links = links or {}
    original = links.get("original") or None
    aihot = links.get("aihot") or None
    return original or aihot, aihot if original else None


def who_what(title: str, source_name: str | None) -> str:
    """Prefer '主体发布了什么' framing when title already starts with the actor."""
    title = (title or "").strip()
    if source_name:
        # If title already names an org, keep title as headline body.
        return title
    return title


def render_item(item: dict, *, flash: bool = False) -> str:
    title = who_what(item.get("title") or "", (item.get("source") or {}).get("name"))
    summary = (item.get("summary") or "").strip()
    source_name = ((item.get("source") or {}).get("name") or "").strip()
    primary, aihot = primary_link(item.get("links"))
    published = to_shanghai(item.get("publishedAt"))

    parts: list[str] = []
    parts.append('<article class="daily-item">')
    if primary:
        parts.append(
            f'<h3><a href="{esc(primary)}" rel="noopener noreferrer">{esc(title)}</a></h3>'
        )
    else:
        parts.append(f"<h3>{esc(title)}</h3>")

    meta_bits: list[str] = []
    if source_name:
        meta_bits.append(f'<span class="daily-source">{esc(source_name)}</span>')
    if published:
        meta_bits.append(
            f'<time datetime="{esc(item.get("publishedAt"))}">{esc(published)}（上海）</time>'
        )
    if meta_bits:
        parts.append('<p class="daily-meta">' + " · ".join(meta_bits) + "</p>")

    if summary and not flash:
        parts.append(f'<p class="daily-summary">{esc(summary)}</p>')

    link_bits: list[str] = []
    if primary:
        host = re.sub(r"^https?://(www\.)?", "", primary).split("/")[0]
        link_bits.append(
            f'<a href="{esc(primary)}" rel="noopener noreferrer">原文（{esc(host)}）</a>'
        )
    if aihot:
        link_bits.append(
            f'<a class="daily-aihot" href="{esc(aihot)}" rel="noopener noreferrer">AIHOT 条目</a>'
        )
    if link_bits:
        parts.append('<p class="daily-links">' + " · ".join(link_bits) + "</p>")

    parts.append("</article>")
    return "\n".join(parts)


def build_body(report: dict, generated_label: str) -> str:
    date = report.get("date") or ""
    links = report.get("links") or {}
    aihot_daily = links.get("aihot") or f"https://aihot.news/daily/{date}"
    lead = report.get("lead") or {}
    sections = report.get("sections") or []
    flashes = report.get("flashes") or []

    # Collect lead item if it also appears in a section — still show as 头条 once
    chunks: list[str] = []
    chunks.append(
        f"""    <section class="hero hero--page">
      <span class="badge">日报</span>
      <h1>AI 日报</h1>
      <p class="lead">
        个人非商业整理：把当天 AI 资讯按分类列出。每条优先链到<strong>原文</strong>；AIHOT 条目作次要核对。
      </p>
      <div class="meta">
        <span>覆盖日期：{esc(date)}（北京时间日历日）</span>
        <span>数据来源：<a href="https://aihot.news" rel="noopener noreferrer">AIHOT</a>
          （<a href="{esc(aihot_daily)}" rel="noopener noreferrer">当日汇总</a>）</span>
        <span>页面生成：{esc(generated_label)}（Asia/Shanghai）</span>
      </div>
    </section>

"""
    )

    # TOC
    toc: list[str] = []
    if lead.get("title"):
        toc.append('<a href="#lead">头条</a>')
    for i, sec in enumerate(sections):
        label = sec.get("label") or f"分类{i+1}"
        short = SECTION_SHORT.get(label, label)
        slug = f"sec-{i}"
        toc.append(f'<a href="#{slug}">{esc(short)}</a>')
    if flashes:
        toc.append('<a href="#flashes">快讯</a>')
    if toc:
        chunks.append(
            '    <nav class="daily-toc" aria-label="本日目录">\n      '
            + " · ".join(toc)
            + "\n    </nav>\n"
        )

    if lead.get("title"):
        # Lead may not have links; try find matching section item
        lead_item = {
            "title": lead.get("title"),
            "summary": lead.get("leadParagraph") or lead.get("summary") or "",
            "source": {},
            "links": {},
        }
        for sec in sections:
            for it in sec.get("items") or []:
                if (it.get("title") or "") == lead.get("title"):
                    lead_item = it
                    break
        chunks.append('    <h2 id="lead">头条</h2>\n')
        chunks.append("    " + render_item(lead_item).replace("\n", "\n    ") + "\n")

    for i, sec in enumerate(sections):
        label = sec.get("label") or "其他"
        short = SECTION_SHORT.get(label, label)
        slug = f"sec-{i}"
        items = sec.get("items") or []
        chunks.append(f'    <h2 id="{slug}">{esc(short)} <span class="daily-sec-full">（{esc(label)}）</span></h2>\n')
        if not items:
            chunks.append("    <p class=\"muted\">本日无条目。</p>\n")
            continue
        for it in items:
            # Skip duplicate of lead in first matching section? Keep all — lead is featured, sections stay complete
            chunks.append("    " + render_item(it).replace("\n", "\n    ") + "\n")

    if flashes:
        chunks.append('    <h2 id="flashes">快讯</h2>\n')
        chunks.append('    <div class="daily-flashes">\n')
        for it in flashes:
            chunks.append("      " + render_item(it, flash=True).replace("\n", "\n      ") + "\n")
        chunks.append("    </div>\n")

    chunks.append(
        """    <div class="note">
      个人非商业整理；转载请注明 AIHOT 与原文。发现问题请走
      <a href="about.html#errata">勘误</a>。
    </div>

    <p class="pager"><a href="../index.html">← 返回首页</a> · <a href="changelog.html">更新日志 →</a></p>
"""
    )
    return "".join(chunks)


def render_page(report: dict, generated_label: str) -> str:
    date = report.get("date") or ""
    lead_title = ((report.get("lead") or {}).get("title") or "AI 资讯整理").strip()
    desc = f"Mogul Desk AI 日报（{date}）：{lead_title}。数据来源 AIHOT，原文优先。"
    body = build_body(report, generated_label)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI 日报 {esc(date)} · Mogul Desk</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="theme-color" content="#161512" />
  <link rel="icon" href="../assets/favicon.svg" type="image/svg+xml" />
  <meta property="og:title" content="AI 日报 {esc(date)} · Mogul Desk" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://prettych.github.io/mogul-desk/pages/ai-daily.html" />
  <meta property="og:locale" content="zh_CN" />
  <meta property="og:site_name" content="Mogul Desk" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="AI 日报 {esc(date)} · Mogul Desk" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <link rel="stylesheet" href="../assets/styles.css" />
  <link rel="canonical" href="https://prettych.github.io/mogul-desk/pages/ai-daily.html" />
</head>
<body>
<a class="skip-link" href="#main">跳到正文</a>
  <header class="site">
    <div class="inner">
      <a class="logo" href="../index.html"><span class="logo-mark" aria-hidden="true">M</span>Mogul <span>Desk</span></a>
      <nav aria-label="主导航">
        <a href="../index.html">首页</a>
        <a href="ai-daily.html" aria-current="page">AI 日报</a>
        <a href="free-static-hosting.html">静态托管</a>
        <a href="free-tts-api.html">TTS API</a>
        <a href="free-llm-api-no-card.html">免绑卡 LLM</a>
        <a href="free-email-api.html">事务邮件</a>
        <a href="changelog.html">更新日志</a>
        <a href="about.html">关于</a>
      </nav>
    </div>
  </header>

  <main id="main" class="wrap" tabindex="-1">
{body}  </main>

  <footer class="site">
    <div class="wrap wrap--wide">
      <p class="footer-brand">Mogul Desk</p>
      <p class="footer-meta">数据来源 <a href="https://aihot.news" rel="noopener noreferrer">AIHOT</a> · 生成 {esc(generated_label)}（Asia/Shanghai） · <a href="about.html">关于本站</a> · <a href="changelog.html">更新日志</a></p>
      <p class="footer-errata">发现问题？<a href="mailto:chengxixi@mail.grokbot.com?subject=Mogul%20Desk%20%E5%8B%98%E8%AF%AF&body=%E9%A1%B5%E9%9D%A2%EF%BC%9Aai-daily%0A%E9%97%AE%E9%A2%98%EF%BC%9A%0A%E5%BB%BA%E8%AE%AE%EF%BC%9A">发勘误邮件</a>（仅勘误 / 纠错，不是客服）。</p>
      <p class="footer-disclaimer">免责：新闻与额度以信源为准；本站个人非商业整理，无流量/收入承诺，未接入联盟链接。</p>
    </div>
  </footer>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Build Mogul Desk AI daily page from JSON.")
    ap.add_argument(
        "json_path",
        nargs="?",
        default=str(DEFAULT_JSON),
        help="Path to aihot-daily.json (default: data/aihot-daily.json)",
    )
    ap.add_argument(
        "-o",
        "--output",
        default=str(OUT_HTML),
        help="Output HTML path (default: pages/ai-daily.html)",
    )
    args = ap.parse_args()

    data = json.loads(Path(args.json_path).read_text(encoding="utf-8"))
    report = data.get("report") or data
    if "date" not in report:
        raise SystemExit("JSON missing report.date")

    now = datetime.now(SHANGHAI)
    generated_label = now.strftime("%Y-%m-%d %H:%M")
    # Prefer fetchedAt from data envelope if present
    fetched = to_shanghai(data.get("fetchedAt"))
    if fetched:
        generated_label = fetched

    html_out = render_page(report, generated_label)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_out, encoding="utf-8")
    print(f"wrote {out_path} ({out_path.stat().st_size} bytes) date={report.get('date')}")


if __name__ == "__main__":
    main()
