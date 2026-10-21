#!/usr/bin/env python3
"""Generate pages/free-static-hosting.html from data/hosting.json."""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hosting.json"
OUT = ROOT / "pages" / "free-static-hosting.html"
BASE = "https://prettych.github.io/htmlTest"
PAGE = "free-static-hosting"
ERRATA = "chengxixi@mail.grokbot.com"

COMMERCIAL_PILL = {
    "allowed": ("pill-ok", "tag-ok"),
    "conditional": ("pill-warn", "tag-warn"),
    "forbidden": ("pill-bad", "tag-bad"),
    "unverified": ("pill-warn", "tag-warn"),
}
OVERAGE_PILL = {
    "soft_limit": ("pill-warn", "tag-warn"),
    "hard_stop": ("pill-bad", "tag-bad"),
    "bill_or_card": ("pill-warn", "tag-warn"),
    "unverified": ("pill-warn", "tag-warn"),
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def mailto(entry_id: str, name: str, commercial: str, overage: str) -> str:
    subj = quote(f"Mogul Desk 勘误 · {PAGE} · {entry_id}")
    body = quote(
        f"页面：{PAGE}.html\n"
        f"id：{entry_id}\n"
        f"名称：{name}\n"
        f"原值：commercial={commercial}; overage={overage}\n"
        f"问题：\n"
        f"官方来源链接：\n"
        f"建议：\n"
    )
    return f"mailto:{ERRATA}?subject={subj}&body={body}"


def status_label(st: str) -> str:
    return {"ok": "已核验", "stale": "待复核", "unverified": "未核实"}.get(st, st)


def row(e: dict) -> str:
    cid, oid = e["commercial"], e["overage"]
    cp, ct = COMMERCIAL_PILL[cid]
    op, ot = OVERAGE_PILL[oid]
    mid = mailto(e["id"], e["name"], cid, oid)
    return f"""        <tr id="row-{esc(e['id'])}" data-entry="{esc(e['id'])}" data-commercial="{esc(cid)}" data-overage="{esc(oid)}" data-verify-status="{esc(e['verifyStatus'])}" data-verified="{esc(e['verified'])}" data-search="{esc(e.get('search',''))}">
          <td><a href="#{esc(e['id'])}">{esc(e['name'])}</a><span class="table-verified" data-verified="{esc(e['verified'])}">核验：{esc(e['verified'])} · {esc(status_label(e['verifyStatus']))}</span></td>
          <td>{esc(e['quota_short'])}</td>
          <td class="{ct}"><span class="pill {cp}">{esc(e['commercial_label'])}</span></td>
          <td class="{ot}"><span class="pill {op}">{esc(e['overage_label'])}</span></td>
          <td>{esc(e['domain_ssl'])}</td>
          <td><a class="errata-link" href="{mid}">勘误</a></td>
        </tr>"""


def article(i: int, e: dict) -> str:
    sc = e["scenario"]
    sources = "\n        ".join(
        f'<a href="{esc(s["url"])}" rel="noopener" target="_blank">{esc(s["label"])}</a>'
        for s in e["sources"]
    )
    mid = mailto(e["id"], e["name"], e["commercial"], e["overage"])
    review = ""
    if e.get("codex_review"):
        review = '<p class="note note--inline"><strong>口径待复核：</strong>商用字段暂标 unverified / 需二次确认，勿当作法律意见。</p>'
    elif e.get("codex_review") is False:
        pass
    note = e.get("codex_review")
    if note and note is not True:
        review = f'<p class="note note--inline"><strong>口径备注：</strong>{esc(str(note))}</p>'
    elif note is True:
        review = '<p class="note note--inline"><strong>口径待复核：</strong>商用字段暂标 unverified，列入 Codex 核口径清单。</p>'

    return f"""    <article class="entry" id="{esc(e['id'])}" data-entry="{esc(e['id'])}" data-commercial="{esc(e['commercial'])}" data-overage="{esc(e['overage'])}" data-verify-status="{esc(e['verifyStatus'])}" data-verified="{esc(e['verified'])}" data-search="{esc(e.get('search',''))}">
      <div class="entry-head">
        <h3>{i}. {esc(e['name'])}</h3>
        <span class="verified" data-verified="{esc(e['verified'])}">核验：{esc(e['verified'])} · {esc(status_label(e['verifyStatus']))}</span>
      </div>
      <p class="one-liner">{esc(e['one_liner'])}</p>
      <dl>
        <dt>场景结论</dt>
        <dd>
          <ul class="scenario-list">
            <li><strong>落地页：</strong>{esc(sc['landing'])}</li>
            <li><strong>作品集：</strong>{esc(sc['portfolio'])}</li>
            <li><strong>卖数字产品：</strong>{esc(sc['digital_product'])}</li>
            <li><strong>SaaS 文档：</strong>{esc(sc['saas_docs'])}</li>
          </ul>
        </dd>
        <dt>免费额度</dt>
        <dd>{esc(e['quota_short'])}</dd>
        <dt>商用（免费档）</dt>
        <dd><code>{esc(e['commercial'])}</code> — {esc(e['commercial_label'])}</dd>
        <dt>超限后果</dt>
        <dd><code>{esc(e['overage'])}</code> — {esc(e['overage_detail'])}</dd>
        <dt>自定义域名 / SSL</dt>
        <dd>{esc(e['domain_ssl'])}</dd>
        <dt>证据句</dt>
        <dd class="evidence">{esc(e['evidence'])}</dd>
      </dl>
      <p class="sources">
        来源：
        {sources}
      </p>
      {review}
      <p class="entry-errata"><a href="{mid}">报告本条过时/错误</a>（预填 id={esc(e['id'])}）</p>
    </article>"""


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    entries = data["entries"]
    verified = data["verified_at"]
    title = data["title"]
    desc = "对照 GitHub Pages、Cloudflare Pages、Vercel Hobby、Netlify Free、Render、Surge、GitLab Pages、Firebase Hosting 的商用限制、额度与超限后果（含核验来源）。"

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
        <a href="free-static-hosting.html" aria-current="page">静态托管</a>
        <a href="free-tts-api.html">TTS API</a>
        <a href="free-llm-api-no-card.html">免绑卡 LLM</a>
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
        面向独立开发者：落地页 / 作品集 / 卖数字产品 / SaaS 文档能不能放免费档？超限是停站还是扣费？数字来自各平台公开文档（核验：{esc(verified)}，Asia/Shanghai）。「未见禁止」≠ 允许商用。
      </p>
    </section>

    <div class="note">
      <strong>口径：</strong>
      <code>commercial</code> = allowed | conditional | forbidden | unverified；
      <code>overage</code> = soft_limit | hard_stop | bill_or_card | unverified。
      筛「可商用」只含 <strong>allowed</strong>；conditional / unverified 默认排除。下结论前请点来源。
    </div>

    <h2>速览</h2>
    <div class="filter-bar" data-compare-root>
      <div class="filter-bar-top">
        <div class="filter-search">
          <label for="filter-q">搜索</label>
          <input type="search" id="filter-q" data-filter-search placeholder="平台名、额度、关键词…" autocomplete="off" />
        </div>
        <div class="filter-meta">
          <span data-filter-count></span>
          <button type="button" class="filter-clear" data-filter-clear>清除</button>
        </div>
      </div>
      <div class="filter-groups">
        <div class="filter-group" data-filter-group="commercial" role="group" aria-label="按商用筛选">
          <span class="filter-group-label">商用</span>
          <button type="button" class="filter-chip is-active" data-filter-value="" aria-pressed="true">全部</button>
          <button type="button" class="filter-chip" data-filter-value="allowed" aria-pressed="false">可商用</button>
          <button type="button" class="filter-chip" data-filter-value="conditional" aria-pressed="false">有条件</button>
          <button type="button" class="filter-chip" data-filter-value="forbidden" aria-pressed="false">不可商用</button>
          <button type="button" class="filter-chip" data-filter-value="unverified" aria-pressed="false">待核实</button>
        </div>
        <div class="filter-group" data-filter-group="overage" role="group" aria-label="按超限后果筛选">
          <span class="filter-group-label">超限</span>
          <button type="button" class="filter-chip is-active" data-filter-value="" aria-pressed="true">全部</button>
          <button type="button" class="filter-chip" data-filter-value="soft_limit" aria-pressed="false">软限制</button>
          <button type="button" class="filter-chip" data-filter-value="hard_stop" aria-pressed="false">硬停</button>
          <button type="button" class="filter-chip" data-filter-value="bill_or_card" aria-pressed="false">扣费或要卡</button>
          <button type="button" class="filter-chip" data-filter-value="unverified" aria-pressed="false">待核实</button>
        </div>
      </div>
      <p class="filter-empty" data-filter-status hidden role="status">没有匹配的条目。试试换关键词，或点「清除」。</p>
    </div>
    <div class="table-scroll" tabindex="0" role="region" aria-label="对照表（可横向滚动）">
    <table class="compare" role="table">
      <thead>
        <tr>
          <th>平台</th>
          <th>免费档要点</th>
          <th>商用</th>
          <th>超限</th>
          <th>域名 / SSL</th>
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
      <strong>选型速记（非赞助）：</strong>
      纯文档/开源展示 → GitHub Pages；
      要明确可商用且能接受积分硬顶 → Netlify Free（额度紧）；
      商用边界清楚但不能用免费档卖货 → 避开 Vercel Hobby / GitHub Pages 商用场景；
      Cloudflare / Firebase → 看 conditional 说明；
      Render / Surge / GitLab → 商用仍待核实。
    </div>

    <p class="pager"><a href="../index.html">← 返回首页</a> · <a href="free-tts-api.html">下一页：免费 TTS API →</a></p>
  </main>

  <footer class="site">
    <div class="wrap wrap--wide">
      <p class="footer-brand">Mogul Desk</p>
      <p class="footer-meta">核验日期：{esc(verified)}（Asia/Shanghai） · <a href="about.html">关于本站</a> · <a href="changelog.html">更新日志</a></p>
      <p class="footer-errata">发现问题？<a href="mailto:{ERRATA}?subject={quote('Mogul Desk 勘误')}&body={quote('页面：free-static-hosting.html\\nid：\\n原值：\\n问题：\\n建议：')}">发勘误邮件</a>（仅勘误 / 纠错，不是客服）。</p>
      <p class="footer-disclaimer">免责：额度与条款以各平台官网为准；本站无流量/收入承诺，未接入联盟链接。本页不是法律意见。</p>
    </div>
  </footer>
  <script src="../assets/compare-filter.js" defer></script>
</body>
</html>
"""
    OUT.write_text(html_out, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {len(entries)} entries)")


if __name__ == "__main__":
    main()
