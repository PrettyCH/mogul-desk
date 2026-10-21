# Mogul Desk（本地 MVP）

静态小站：挑会反复被搜的「无聊」垂直方向，做可核验的对照页。  
**没有流量数字，没有收入承诺，没有已谈成的联盟。**

核验时区：Asia/Shanghai · 内容页日期：2026-10-21

## Niche（一句话）

个人开发者实用对照三件套：

1. **免费静态托管**额度 / 商用条款 / 自定义域名  
2. **免费 TTS / 语音合成 API**额度与是否绑卡  
3. **无需绑卡（或写明要绑卡）的免费 LLM API**短名单  

## 为什么选这个方向（需求证据）

已有真实对照与讨论，说明搜索意图存在，但多数文章不强调「商用条款」、积分制或「绑不绑卡」：

1. 中文对照：[網站放 GitHub、Vercel 還是 Cloudflare？](https://jiangyude.com/articles/github-vercel-cloudflare-compare/)（额度 + 商用限制）
2. 中文横评：[Vercel / Cloudflare Pages / GitHub Pages 2026](https://crook-blog.vercel.app/blog/vercel-vs-cloudflare-pages-vs-github-pages/)
3. 英文汇总：[Best Free Static Site Hosting 2026](https://devshot.co/reviews/best-free-static-hosting)、[Free Cloud Hosting 2026](https://snapdeploy.dev/blog/free-cloud-deployment-platforms-2026-comparison)

本站刻意做成「可点进官方文档核对」的目录型页面，而不是复述营销文案。

## 文件结构

```
mogul-site/
├── index.html                         # 站点说明 + 目录（3 篇）
├── assets/styles.css                  # 简洁深色样式，移动端可读
├── pages/
│   ├── free-static-hosting.html       # 静态托管对照（8 条）
│   ├── free-tts-api.html              # 免费 TTS API 对照（8 条）
│   └── free-llm-api-no-card.html      # 免绑卡 LLM API 短名单（8 条）
└── README.md                          # 本文件
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

## 公开部署还缺什么

当前只有 box 上的文件，**尚未**：

- Git 远程仓库（GitHub / GitLab）
- 绑定域名与 DNS
- Cloudflare Pages / GitHub Pages / 其他托管账号上的项目

推荐路径（任选其一，与内容页一致）：

1. **Cloudflare Pages**：适合以后可能挂联盟/广告的商用向静态站（仍需自己读 ToS）。
2. **GitHub Pages**：适合开源文档展示；**不要**拿免费档跑在线生意站。
3. **GitLab Pages**：若代码已在 GitLab。

典型步骤概要：

```text
git init && git add . && git commit -m "Initial Mogul Desk MVP"
# 推到 GitHub 后：Settings → Pages，或接 Cloudflare Pages「Connect Git」
# 自定义域名：在托管后台填域名，再在域名商处加 CNAME/A 记录
```

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
| 无需绑卡的免费 LLM API 短名单 | **已发布** → `pages/free-llm-api-no-card.html`（8 条；跳过 GitHub Models 已退役、Cerebras 强制绑卡试用、DeepSeek 需预充等） |
| 后续可写 | 免费 STT / 语音识别额度对照；「注册赠金 vs 长期免费」总表（跨厂商） |

## 免责

平台额度与条款随时变更。本站内容供学习与选型参考，不构成投资、法律或商务建议。
