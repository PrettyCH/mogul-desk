#!/usr/bin/env python3
"""Generate pages/free-llm-api-no-card.html from data/llm.json."""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "llm.json"
OUT = ROOT / "pages" / "free-llm-api-no-card.html"
BASE = "https://prettych.github.io/htmlTest"
PAGE = "free-llm-api-no-card"
ERRATA = "chengxixi@mail.grokbot.com"

CARD_PILL = {
    "none": ("pill-ok", "tag-ok"),
    "required": ("pill-bad", "tag-bad"),
    "conditional": ("pill-warn", "tag-warn"),
    "unverified": ("pill-warn", "tag-warn"),
}
FREE_PILL = {
    "recurring": ("pill-ok", "tag-ok"),
    "trial_credit": ("pill-warn", "tag-warn"),
    "none": ("pill-bad", "tag-bad"),
    "unverified": ("pill-warn", "tag-warn"),
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def mailto(entry_id: str, name: str, card: str, free_type: str) -> str:
    subj = quote(f"Mogul Desk 勘误 · {PAGE} · {entry_id}")
    body = quote(
        f"页面：{PAGE}.html\n"
        f"id：{entry_id}\n"
        f"名称：{name}\n"
        f"原值：card={card}; freeType={free_type}\n"
        f"问题：\n"
        f"官方来源链接：\n"
        f"建议：\n"
    )
    return f"mailto:{ERRATA}?subject={subj}&body={body}"


def status_label(st: str) -> str:
    return {"ok": "已核验", "stale": "待复核", "unverified": "未核实"}.get(st, st)


def row(e: dict) -> str:
    cid, ft = e["card"], e["freeType"]
    cp, ct = CARD_PILL[cid]
    fp, ft_tag = FREE_PILL[ft]
    mid = mailto(e["id"], e["name"], cid, ft)
    return f"""        <tr id="row-{esc(e['id'])}" data-entry="{esc(e['id'])}" data-card="{esc(cid)}" data-freetype="{esc(ft)}" data-verify-status="{esc(e['verifyStatus'])}" data-verified="{esc(e['verified'])}" data-search="{esc(e.get('search',''))}">
          <td><a href="#{esc(e['id'])}">{esc(e['name'])}</a><span class="table-verified" data-verified="{esc(e['verified'])}">核验：{esc(e['verified'])} · {esc(status_label(e['verifyStatus']))}</span></td>
          <td>{esc(e['quota_short'])}<br /><span class="pill {fp}">{esc(e['free_type_label'])}</span></td>
          <td class="{ct}"><span class="pill {cp}">{esc(e['card_label'])}</span></td>
          <td><a class="errata-link" href="{mid}">勘误</a></td>
        </tr>"""


def article(i: int, e: dict) -> str:
    sources = "\n        ".join(
        f'<a href="{esc(s["url"])}" rel="noopener" target="_blank">{esc(s["label"])}</a>'
        for s in e["sources"]
    )
    mid = mailto(e["id"], e["name"], e["card"], e["freeType"])
    trial = ""
    if e.get("trial_detail"):
        trial = f"""        <dt>试用金用尽 / 到期</dt>
        <dd>{esc(e['trial_detail'])}</dd>"""
    return f"""    <article class="entry" id="{esc(e['id'])}" data-entry="{esc(e['id'])}" data-card="{esc(e['card'])}" data-freetype="{esc(e['freeType'])}" data-verify-status="{esc(e['verifyStatus'])}" data-verified="{esc(e['verified'])}" data-search="{esc(e.get('search',''))}">
      <div class="entry-head">
        <h3>{i}. {esc(e['name'])}</h3>
        <span class="verified" data-verified="{esc(e['verified'])}">核验：{esc(e['verified'])} · {esc(status_label(e['verifyStatus']))}</span>
      </div>
      <p class="one-liner">{esc(e['one_liner'])}</p>
      <dl>
        <dt>用途</dt>
        <dd>{esc(e['use_case'])}</dd>
        <dt>官方限额</dt>
        <dd><code>freeType={esc(e['freeType'])}</code> — {esc(e['quota_detail'])}</dd>
{trial}
        <dt>是否绑卡</dt>
        <dd><code>card={esc(e['card'])}</code> — {esc(e['card_detail'])}</dd>
        <dt>证据句</dt>
        <dd class="evidence">{esc(e['evidence'])}</dd>
      </dl>
      <p class="sources">
        来源：
        {sources}
      </p>
      <p class="entry-errata"><a href="{mid}">报告本条过时/错误</a>（预填 id={esc(e['id'])}）</p>
    </article>"""


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    entries = data["entries"]
    verified = data["verified_at"]
    title = data["title"]
    desc = "Gemini、Groq、OpenRouter、Workers AI、Mistral、NVIDIA、Fireworks、SiliconFlow 等免费/起步积分与是否绑卡对照（可核验）。"

    list_items = ",\n    ".join(
        f"""{{
      "@type": "ListItem",
      "position": {i},
      "name": {json.dumps(e["name"], ensure_ascii=False)},
      "url": "{BASE}/pages/{PAGE}.html#{e['id']}"
    }}"""
        for i, e in enumerate(entries, 1)
    )
    rows = "\n".join(row(e) for e in entries)
    articles = "\n\n".join(article(i, e) for i, e in enumerate(entries, 1))

    dist = {}
    for e in entries:
        dist[e["freeType"]] = dist.get(e["freeType"], 0) + 1

    html_out = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)} · Mogul Desk</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="theme-color" content="#161512" />
  <link rel="icon" href="../assets/favicon.svg" type="image/svg+xml" />
  <link rel="canonical" href="{BASE}/pages/{PAGE}.html" />
  <meta property="og:title" content="{esc(title)} · Mogul Desk" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{BASE}/pages/{PAGE}.html" />
  <meta property="og:locale" content="zh_CN" />
  <meta property="og:site_name" content="Mogul Desk" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{esc(title)} · Mogul Desk" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <link rel="stylesheet" href="../assets/styles.css" />
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": {json.dumps(title, ensure_ascii=False)},
  "description": {json.dumps(desc, ensure_ascii=False)},
  "numberOfItems": {len(entries)},
  "itemListElement": [
    {list_items}
  ]
}}
  </script>
</head>
<body>
<a class="skip-link" href="#main">跳到正文</a>
  <header class="site">
    <div class="inner">
      <a class="logo" href="../index.html"><span class="logo-mark" aria-hidden="true">M</span>Mogul <span>Desk</span></a>
      <nav aria-label="主导航">
        <a href="../index.html">首页</a>
        <a href="ai-daily.html">AI 日报</a>
        <a href="free-static-hosting.html">静态托管</a>
        <a href="free-tts-api.html">TTS API</a>
        <a href="free-llm-api-no-card.html" aria-current="page">免绑卡 LLM</a>
        <a href="free-email-api.html">事务邮件</a>
        <a href="changelog.html">更新日志</a>
        <a href="about.html">关于</a>
      </nav>
    </div>
  </header>

  <main id="main" class="wrap wrap--wide" tabindex="-1">
    <section class="hero hero--page">
      <span class="badge">对照页</span>
      <h1>{esc(title)}</h1>
      <p class="lead">
        只列官方公开限额与入口。核验：<strong>{esc(verified)}（Asia/Shanghai）</strong>。枚举：<code>card</code>=none|required|conditional|unverified；<code>freeType</code>=recurring|trial_credit|none|unverified。别把试用金当成周期免费。
      </p>
    </section>

    <div class="note">
      <strong>怎么读：</strong>筛「免绑卡起步」= <code>card=none</code>；筛「周期免费」= <code>freeType=recurring</code>（持续按日/月刷新，不承诺永久）；「试用金」= <code>trial_credit</code>（用尽或到期即停）。文案与托管页的「可商用 / 超限」筛选分开。RPM/RPD 以各控制台 Limits 为准。
    </div>

    <h2>速览</h2>
    <div class="filter-bar" data-compare-root>
      <div class="filter-bar-top">
        <div class="filter-search">
          <label for="filter-q">搜索</label>
          <input type="search" id="filter-q" data-filter-search placeholder="服务名、额度、关键词…" autocomplete="off" />
        </div>
        <div class="filter-meta">
          <span data-filter-count></span>
          <button type="button" class="filter-clear" data-filter-clear>清除</button>
        </div>
      </div>
      <div class="filter-groups">
        <div class="filter-group" data-filter-group="card" role="group" aria-label="按是否绑卡筛选">
          <span class="filter-group-label">绑卡</span>
          <button type="button" class="filter-chip is-active" data-filter-value="" aria-pressed="true">全部</button>
          <button type="button" class="filter-chip" data-filter-value="none" aria-pressed="false">免绑卡起步</button>
          <button type="button" class="filter-chip" data-filter-value="conditional" aria-pressed="false">有条件</button>
          <button type="button" class="filter-chip" data-filter-value="required" aria-pressed="false">需要绑卡</button>
          <button type="button" class="filter-chip" data-filter-value="unverified" aria-pressed="false">待核实</button>
        </div>
        <div class="filter-group" data-filter-group="freetype" role="group" aria-label="按免费类型筛选">
          <span class="filter-group-label">免费类型</span>
          <button type="button" class="filter-chip is-active" data-filter-value="" aria-pressed="true">全部</button>
          <button type="button" class="filter-chip" data-filter-value="recurring" aria-pressed="false">周期免费</button>
          <button type="button" class="filter-chip" data-filter-value="trial_credit" aria-pressed="false">试用金</button>
          <button type="button" class="filter-chip" data-filter-value="none" aria-pressed="false">无免费档</button>
          <button type="button" class="filter-chip" data-filter-value="unverified" aria-pressed="false">待核实</button>
        </div>
      </div>
      <p class="filter-empty" data-filter-status hidden role="status">没有匹配的条目。试试换关键词，或点「清除」。</p>
    </div>
    <div class="table-scroll" tabindex="0" role="region" aria-label="对照表（可横向滚动）">
    <table class="compare" role="table">
      <thead>
        <tr>
          <th>服务</th>
          <th>免费要点</th>
          <th>绑卡</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
{rows}
      </tbody>
    </table>
    </div>

    <h2 id="entries">逐条说明</h2>

{articles}

    <div class="note">
      <strong>明确跳过 / 不写进「免绑卡长期免费」：</strong>
      <ul>
        <li><strong>GitHub Models</strong>：官方文档写明已于 2026-07-30 退役。</li>
        <li><strong>Cerebras Free Trial</strong>：官方写明需先添加已验证支付方式才发试用金，且无永久免费档。</li>
        <li><strong>DeepSeek 官方 API</strong>：需预充值余额，无「长期免费用量」公开档。</li>
        <li><strong>Hugging Face Inference Providers</strong>：免费用户月度积分政策易变，本页不收录易过期数字。</li>
      </ul>
    </div>

    <p class="pager"><a href="free-tts-api.html">← 上一页：免费 TTS API</a> · <a href="../index.html">首页</a> · <a href="free-email-api.html">下一页：事务邮件 API →</a></p>
  </main>

  <footer class="site">
    <div class="wrap wrap--wide">
      <p class="footer-brand">Mogul Desk</p>
      <p class="footer-meta">核验日期：{esc(verified)}（Asia/Shanghai） · <a href="about.html">关于本站</a> · <a href="changelog.html">更新日志</a></p>
      <p class="footer-errata">发现问题？<a href="mailto:{ERRATA}?subject={quote('Mogul Desk 勘误')}&body={quote('页面：free-llm-api-no-card.html\\nid：\\n原值：\\n问题：\\n建议：')}">发勘误邮件</a>（仅勘误 / 纠错，不是客服）。</p>
      <p class="footer-disclaimer">免责：额度与条款以各平台官网为准；本站无流量/收入承诺，未接入联盟链接。</p>
    </div>
  </footer>
  <script src="../assets/compare-filter.js" defer></script>
</body>
</html>
"""
    OUT.write_text(html_out, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {len(entries)} entries)")
    print("freeType distribution:", dist)


if __name__ == "__main__":
    main()
