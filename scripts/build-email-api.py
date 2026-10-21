#!/usr/bin/env python3
"""Generate pages/free-email-api.html from data/email-api.json."""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "email-api.json"
OUT = ROOT / "pages" / "free-email-api.html"
BASE = "https://prettych.github.io/htmlTest"
PAGE = "free-email-api"
ERRATA = "chengxixi@mail.grokbot.com"

CARD_PILL = {
    "none": ("pill-ok", "tag-ok"),
    "required": ("pill-bad", "tag-bad"),
    "conditional": ("pill-warn", "tag-warn"),
    "unverified": ("pill-warn", "tag-warn"),
}
COMM_PILL = {
    "allowed": ("pill-ok", "tag-ok"),
    "conditional": ("pill-warn", "tag-warn"),
    "forbidden": ("pill-bad", "tag-bad"),
    "unverified": ("pill-warn", "tag-warn"),
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def mailto(entry_id: str, name: str, card: str, commercial: str) -> str:
    subj = quote(f"Mogul Desk 勘误 · {PAGE} · {entry_id}")
    body = quote(
        f"页面：{PAGE}.html\n"
        f"id：{entry_id}\n"
        f"名称：{name}\n"
        f"原值：card={card}; commercial={commercial}\n"
        f"问题：\n"
        f"官方来源链接：\n"
        f"建议：\n"
    )
    return f"mailto:{ERRATA}?subject={subj}&body={body}"


def status_label(st: str) -> str:
    return {"ok": "已核验", "stale": "待复核", "unverified": "未核实"}.get(st, st)


def row(e: dict) -> str:
    cid, mid_c = e["card"], e["commercial"]
    cp, ct = CARD_PILL[cid]
    mp, mt = COMM_PILL[mid_c]
    mid = mailto(e["id"], e["name"], cid, mid_c)
    return f"""        <tr id="row-{esc(e['id'])}" data-entry="{esc(e['id'])}" data-card="{esc(cid)}" data-commercial="{esc(mid_c)}" data-verify-status="{esc(e['verifyStatus'])}" data-verified="{esc(e['verified'])}" data-search="{esc(e.get('search',''))}">
          <td><a href="#{esc(e['id'])}">{esc(e['name'])}</a><span class="table-verified" data-verified="{esc(e['verified'])}">核验：{esc(e['verified'])} · {esc(status_label(e['verifyStatus']))}</span></td>
          <td>{esc(e['quota_short'])}</td>
          <td class="{ct}"><span class="pill {cp}">{esc(e['card_label'])}</span></td>
          <td class="{mt}"><span class="pill {mp}">{esc(e['commercial_label'])}</span></td>
          <td><a class="errata-link" href="{mid}">勘误</a></td>
        </tr>"""


def article(i: int, e: dict) -> str:
    sources = "\n        ".join(
        f'<a href="{esc(s["url"])}" rel="noopener" target="_blank">{esc(s["label"])}</a>'
        for s in e["sources"]
    )
    mid = mailto(e["id"], e["name"], e["card"], e["commercial"])
    return f"""    <article class="entry" id="{esc(e['id'])}" data-entry="{esc(e['id'])}" data-card="{esc(e['card'])}" data-commercial="{esc(e['commercial'])}" data-verify-status="{esc(e['verifyStatus'])}" data-verified="{esc(e['verified'])}" data-search="{esc(e.get('search',''))}">
      <div class="entry-head">
        <h3>{i}. {esc(e['name'])}</h3>
        <span class="verified" data-verified="{esc(e['verified'])}">核验：{esc(e['verified'])} · {esc(status_label(e['verifyStatus']))}</span>
      </div>
      <p class="one-liner">{esc(e['one_liner'])}</p>
      <dl>
        <dt>用途</dt>
        <dd>{esc(e['use_case'])}</dd>
        <dt>日额度</dt>
        <dd>{esc(e['quota_day'])}</dd>
        <dt>月额度</dt>
        <dd>{esc(e['quota_month'])}</dd>
        <dt>额度说明</dt>
        <dd>{esc(e['quota_detail'])}</dd>
        <dt>是否绑卡</dt>
        <dd><code>card={esc(e['card'])}</code> — {esc(e['card_detail'])}</dd>
        <dt>商用发信（免费档）</dt>
        <dd><code>commercial={esc(e['commercial'])}</code> — {esc(e['commercial_detail'])}</dd>
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
    desc = "Resend、Mailgun、Postmark、Amazon SES、Brevo、SendGrid、ZeptoMail 等免费/试用事务邮件 API：免绑卡、月日额度、可否商用发信（可核验）。"

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
        <a href="free-static-hosting.html">静态托管</a>
        <a href="free-tts-api.html">TTS API</a>
        <a href="free-llm-api-no-card.html">免绑卡 LLM</a>
        <a href="free-email-api.html" aria-current="page">事务邮件</a>
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
        静态站上线后下一步常搜「免费发验证码邮件」。本页对照事务邮件 API 的免绑卡、日/月额度与免费档能否商用发信。核验：{esc(verified)}（Asia/Shanghai）。线索可参考 free-for-dev，数字一律以官方文档为准。
      </p>
    </section>

    <div class="note">
      <strong>口径：</strong>
      <code>card</code> = none | required | conditional | unverified；
      <code>commercial</code> = allowed | conditional | forbidden | unverified。
      筛「免绑卡」= card=none；筛「可商用」只含 <strong>allowed</strong>（conditional 如带品牌贴纸的 Brevo Free 默认排除）。别把 SendGrid 试用当成永久免费档。
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
        <div class="filter-group" data-filter-group="commercial" role="group" aria-label="按商用发信筛选">
          <span class="filter-group-label">商用发信</span>
          <button type="button" class="filter-chip is-active" data-filter-value="" aria-pressed="true">全部</button>
          <button type="button" class="filter-chip" data-filter-value="allowed" aria-pressed="false">可商用</button>
          <button type="button" class="filter-chip" data-filter-value="conditional" aria-pressed="false">有条件</button>
          <button type="button" class="filter-chip" data-filter-value="forbidden" aria-pressed="false">不可商用</button>
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
          <th>免费档要点</th>
          <th>绑卡</th>
          <th>商用发信</th>
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
      要长期免绑卡 + 月量尚可 → Resend Free（3k/月·100/日）或 Brevo（300/日，带品牌）；
      只要测送达 → Postmark Free（100/月）或 Mailgun（100/日）；
      已在 AWS → SES（按量 + Free Tier credits，新客户无旧 3000/月专属档）；
      别把 SendGrid 60 天试用写成「永久免费」。国内厂商（如阿里云邮件推送）待官方公开免费档文档可抓取后再补。
    </div>

    <p class="pager"><a href="free-llm-api-no-card.html">← 上一页：免绑卡 LLM</a> · <a href="../index.html">首页</a></p>
  </main>

  <footer class="site">
    <div class="wrap wrap--wide">
      <p class="footer-brand">Mogul Desk</p>
      <p class="footer-meta">核验日期：{esc(verified)}（Asia/Shanghai） · <a href="about.html">关于本站</a> · <a href="changelog.html">更新日志</a></p>
      <p class="footer-errata">发现问题？<a href="mailto:{ERRATA}?subject={quote('Mogul Desk 勘误')}&body={quote('页面：free-email-api.html\\nid：\\n原值：\\n问题：\\n建议：')}">发勘误邮件</a>（仅勘误 / 纠错，不是客服）。</p>
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
