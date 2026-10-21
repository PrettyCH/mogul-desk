# 托管页周检清单（内部，可不公开）

时区：Asia/Shanghai。超过 30 天未核对 → `verifyStatus=stale`。

## 每周（试用金无关；看政策跳变）

| ID | 查什么 | 主要 URL |
| --- | --- | --- |
| github-pages | 商用禁令句是否还在；带宽/站点大小软上限 | https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits |
| vercel-hobby | Fair Use「non-commercial」；Hobby 表额度 | https://vercel.com/docs/limits/fair-use-guidelines · https://vercel.com/docs/plans/hobby |
| cloudflare-pages | builds/文件数；ToS 2.2.1 是否仍无商用禁令 | https://developers.cloudflare.com/pages/platform/limits/ · https://www.cloudflare.com/terms/ |
| netlify-free | 300 credits / hard limit；博文「commercial projects」是否仍有效 | https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/ |
| render-static | Hobby 5 GB；无卡停服 vs 有卡计费 | https://render.com/docs/outbound-bandwidth |
| surge | Pricing 是否仍无商用/超限细则 | https://surge.sh/pricing |
| gitlab-pages | 1 GB / 150 域名；ToS 商用句 | https://docs.gitlab.com/user/gitlab_com/ |
| firebase-hosting | Spark 10 GB 存储/传输；超限禁用 | https://firebase.google.com/docs/hosting/usage-quotas-pricing |

## 口径规则

- `commercial=allowed` 必须有**正许**或官方明确可商用句；「未见禁止」→ `unverified` 或 `conditional`。
- 筛「可商用」只匹配 `allowed`。
- 仅刷新 `verified` 日期、字段未变 → **不写 changelog**。
- 字段旧→新必须带依据 URL 进 changelog。

## 待 Codex 核口径（2026-10-21）

1. Netlify Free：`allowed`（依据 2023 博文）是否应降为 `conditional`（credit-based 文档只强调 experiments）
2. Render Static：`unverified` — 是否有 ToS 正许/禁止
3. Surge.sh：`unverified` / overage `unverified`
4. GitLab Pages：`unverified`
5. Cloudflare Pages：现 `conditional` — 是否可升 `allowed`（ToS 无禁令 + 社区确认）
