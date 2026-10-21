# Mogul Desk（本地 MVP）

静态小站：挑会反复被搜的「无聊」垂直方向，做可核验的对照页。  
**没有流量数字，没有收入承诺，没有已谈成的联盟。**

核验时区：Asia/Shanghai · 内容页日期：2026-10-21

## Niche（一句话）

个人开发者实用对照三件套：

1. **免费静态托管**额度 / 商用条款 / 自定义域名  
2. **免费 TTS / 语音合成 API**额度与是否绑卡  
3. **无需绑卡（或写明要绑卡）的免费 LLM API**短名单  
4. **免费事务邮件 API**（免绑卡 / 月日额度 / 商用发信）  

## 为什么选这个方向（需求证据）

已有真实对照与讨论，说明搜索意图存在，但多数文章不强调「商用条款」、积分制或「绑不绑卡」：

1. 中文对照：[網站放 GitHub、Vercel 還是 Cloudflare？](https://jiangyude.com/articles/github-vercel-cloudflare-compare/)（额度 + 商用限制）
2. 中文横评：[Vercel / Cloudflare Pages / GitHub Pages 2026](https://crook-blog.vercel.app/blog/vercel-vs-cloudflare-pages-vs-github-pages/)
3. 英文汇总：[Best Free Static Site Hosting 2026](https://devshot.co/reviews/best-free-static-hosting)、[Free Cloud Hosting 2026](https://snapdeploy.dev/blog/free-cloud-deployment-platforms-2026-comparison)

本站刻意做成「可点进官方文档核对」的目录型页面，而不是复述营销文案。

## 文件结构

```
mogul-site/
├── index.html                         # 站点说明 + 目录
├── robots.txt                         # 允许抓取 + Sitemap 指向
├── sitemap.xml                        # 本地写好的 Pages URL（部署后可改域名）
├── assets/
│   ├── styles.css                     # 深色样式；筛选条；打印友好
│   ├── compare-filter.js              # 对照表筛选 / 搜索（无构建）
│   └── favicon.svg                    # 极简图标
├── pages/
│   ├── free-static-hosting.html       # 静态托管对照（8 条，可筛商用）
│   ├── free-tts-api.html              # 免费 TTS API 对照（8 条，可筛绑卡）
│   ├── free-llm-api-no-card.html      # 免绑卡 LLM（8 条；card / freeType）
│   ├── free-email-api.html            # 事务邮件 API（7 条；绑卡 / 商用）
│   ├── ai-daily.html                  # AIHOT 日报
│   ├── changelog.html                 # 更新日志
│   └── about.html                     # 本站说明 + 勘误入口
├── data/
│   ├── hosting.json / tts.json / llm.json / email-api.json / aihot-daily.json
├── scripts/
│   ├── build-hosting.py / build-tts.py / build-llm.py / build-email-api.py / build-ai-daily.py
└── README.md
```

## 功能（2026-10-21）

- 对照表：**状态筛选** + **关键词搜索**（过滤表行与下方条目卡；无匹配有空状态）
- 每条 **核验：2026-10-21**（`data-verified`，表行 + 条目卡）
- **更新日志**、页脚 / 关于页 **勘误 mailto**
- Open Graph + JSON-LD（WebSite / ItemList）；skip link

## 重建对照页

```bash
python3 scripts/build-hosting.py
python3 scripts/build-tts.py
python3 scripts/build-llm.py
python3 scripts/build-email-api.py
```

## 本地预览

在仓库根目录（本目录）执行：

```bash
cd /workspace/mogul-site
python3 -m http.server 8765
```

浏览器打开：`http://127.0.0.1:8765/`  
（短时预览即可；不要当作长期服务。）

也可用任意静态服务器，或直接用浏览器打开 `index.html`（部分浏览器对本地相对路径限制更严，推荐 http.server）。

## 明天部署清单（PrettyCH/htmlTest + GitHub Pages）

目标公开地址：`https://prettych.github.io/htmlTest/`

**当前卡点：** Cursor / Grok Bot 侧的 GitHub 令牌对 `PrettyCH/htmlTest` **没有写权限**（推送与 create/update file 均失败）。需要你在电脑上给仓库授权，或本机手动推送。

1. **授权或本机推送**  
   - 在 Cursor 里给 `PrettyCH/htmlTest` 开仓库写权限；或  
   - 本机：把 `/workspace/mogul-site/` 内容放到仓库**根目录**（不要多套一层 `mogul-site/`），`git push` 到默认分支（`main` 或 `master`）。
2. **打开 GitHub Pages**  
   - 仓库 Settings → Pages → Source 选 `Deploy from a branch` → Branch：`main`（或 `master`）+ `/ (root)` → Save。  
   - 等一两分钟后打开：`https://prettych.github.io/htmlTest/`
3. **可选核对**  
   - 点开三篇对照页与「关于」；确认 CSS / favicon 加载正常。  
   - 若以后换自定义域名，改 `robots.txt` 与 `sitemap.xml` 里的绝对 URL。

> 说明：GitHub Pages 免费档**不允许**当在线生意站主机（见本站「静态托管」页）。本站当前是文档型对照页，一般符合「项目文档」用途；若以后挂联盟/卖货，请改 Cloudflare Pages 等更合适的托管。

## 可选联盟计划（仅公开入口，未申请、未谈成）

以后若要变现，应先读各计划规则再申请。下面只列公开页面 URL：

| 方向 | 公开计划页 |
| --- | --- |
| Cloudflare 合作伙伴 | https://www.cloudflare.com/partners/ |
| Namecheap Affiliate | https://www.namecheap.com/affiliate-program/ |
| Porkbun Affiliate | https://porkbun.com/affiliate |
| Dynadot Affiliate | https://www.dynadot.com/community/affiliate |
| Hover Affiliate | https://www.hover.com/affiliates |

**本 MVP 未嵌入任何联盟链接、未注册上述计划。**

## Next pages（状态）

| 候选 | 状态 |
| --- | --- |
| 免费 TTS / 语音合成 API 额度对照 | **已发布** → `pages/free-tts-api.html`（8 条；跳过火山：官方计费页核验失败） |
| 无需绑卡的免费 LLM API 短名单 | **已发布** → `pages/free-llm-api-no-card.html`（8 条；recurring×6 / trial_credit×2） |
| 免费事务邮件 API | **已发布** → `pages/free-email-api.html`（7 条） |
| 关于本站 | **已发布** → `pages/about.html` |
| 后续可写 | 免费 STT；国内邮件推送公开免费档（文档可抓取后再补） |

## 免责

平台额度与条款随时变更。本站内容供学习与选型参考，不构成投资、法律或商务建议。

## AI 日报（AIHOT）

- 数据：`data/aihot-daily.json`
- 生成页：`pages/ai-daily.html`（由脚本覆盖写入）
- 一键拉取并重建（在本机 / box）：

```bash
./scripts/fetch-ai-daily.sh          # 默认今天（Asia/Shanghai）
./scripts/fetch-ai-daily.sh 2026-10-21
# 或只重建：
python3 scripts/build-ai-daily.py
```

只 GET `aihot.news`；页面里每条优先链原文，AIHOT 条目为次要。个人非商业整理。

