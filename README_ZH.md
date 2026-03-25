# AI News Radar

> **自动收集、摘要、分类AI新闻的个人智能仪表板 — 74个来源、35个LLM、50+功能**

**[English](./README.md) / [Korean](./README_KO.md) / [Japanese](./README_JA.md) / Chinese**

---

## 这是什么？

AI News Radar是一个**个人仪表板**，自动从全球收集AI新闻，AI进行**摘要、分类和重要性评分**。支持**35个LLM平台**（大部分免费）、**Web+桌面**双模式、可自动发布到**5个社交平台**。

**简单来说：** 不再每天浏览数十个AI新闻网站，这个应用替你完成，只展示重要内容。

---

## 仪表板（5个标签页）

| 标签页 | 内容 |
|--------|------|
| **Dashboard** | 简报 + 关注领域 + 分类过滤 + 情感图表 + 周报 + 邮件通讯 |
| **News Feed** | 全部新闻 / 搜索 / 收藏 / 时间线 |
| **AI** | 新闻聊天 / AI术语表 |
| **Insights** | 工具对比 / 趋势 / AI辩论 / 周报 |
| **Share** | 社交发布 / AI内容生成 / 导出 |

---

## 主要功能（50+）

### 仪表板
| 功能 | 说明 |
|------|------|
| 每日简报 | AI每天自动生成"今日AI新闻 TOP 5" |
| 关注领域简报 | 图像/视频、Vibe编程、本体论分领域定制简报 |
| 分类过滤 | 9个分类一键过滤（显示数量） |
| 情感图表 | 正面/中立/负面比例的Plotly图表 |
| 语音简报 | 用AI语音收听简报（女声/男声可选） |
| 周报 | 自动生成趋势+领域动态+预测报告 |
| 邮件通讯 | 日报/周报自动邮件发送（SMTP） |

### 新闻流
| 功能 | 说明 |
|------|------|
| 74来源自动收集 | 从全球74个RSS来源并行爬取自动收集 |
| AI摘要 | 每篇文章3行摘要 |
| 9个分类 | 工具、研究、趋势、教程、商业、**图像/视频**、**Vibe编程**、**本体论**、其他 |
| 重要度评分 | 每篇文章1-5星评级 |
| 情感分析 | 正面 / 中立 / 负面 标签 |
| 事实核查 | 多源交叉验证（"3家媒体确认" vs "独家报道"） |
| 重复合并 | 相同新闻自动合并 |
| 关键词监控 | 包含追踪关键词的新闻高亮显示 |
| 应用内阅读 | 在仪表板内阅读文章（无广告） |
| 搜索 | 关键词+分类+情感+已读状态过滤 |
| 收藏+备注 | 保存文章+添加个人备注 |
| 分页 | 每页10条，翻页导航 |
| 时间线视图 | 按今天 / 昨天 / 本周浏览 |

### AI功能
| 功能 | 说明 |
|------|------|
| AI聊天 | 用自然语言询问已收集的新闻 |
| AI术语表 | 自动将专业术语用通俗语言解释 |
| AI辩论 | "Midjourney vs Flux" — AI生成正反方论据+结论 |
| AI内容生成 | 自动撰写推文、长推文、Instagram说明、博客、LinkedIn帖子（5种） |
| 智能提醒 | 检测到监控关键词时桌面通知 |
| 工具对比 | 19个AI工具按分类对比新闻提及量+情感图表 |
| 趋势图表 | 关键词时序图表+热门上升关键词 |

### 分享+导出
| 功能 | 说明 |
|------|------|
| 社交自动发布 | 向X、Telegram、Discord、Threads、Instagram发布卡片新闻 |
| 卡片新闻 | 自动生成1080x1080卡片图片（暗色主题，按分类配色） |
| 导出 | Markdown / PDF 下载 |

### 桌面应用+自动化
| 功能 | 说明 |
|------|------|
| 桌面应用 | 原生窗口（pywebview）+ 系统托盘 + 后台通知 |
| GitHub Actions | 每天3次自动收集处理（CI/CD） |
| 一键流水线 | 收集→AI处理→生成简报一键执行 |
| 发布追踪 | 自动监控主要AI工具的新版本和更新 |
| 自动翻译 | 新闻文章多语言翻译支持 |

---

## 74个新闻来源

| 分类 | 数量 | 示例 |
|------|------|------|
| 通用AI | 26 | TechCrunch, The Verge, MIT Tech Review, Wired, ZDNET, Ben's Bites |
| 图像/视频 | 20 | Stability AI, Civitai, Runway, Reddit (StableDiffusion, midjourney, flux_ai, comfyui) |
| Vibe编程 | 19 | Cursor, GitHub, Anthropic, Simon Willison, Reddit (vibecoding, ClaudeAI, cursor) |
| 本体论 | 9 | Neo4j, Stardog, W3C, Reddit (semanticweb, KnowledgeGraphs) |

---

## 35个LLM平台

只需**任意一个**平台的API密钥即可运行：

| 层级 | 平台 |
|------|------|
| **免费（推荐）** | Gemini, Groq, Cerebras, SambaNova, xAI, Mistral, Cohere, HuggingFace, NVIDIA, Cloudflare, Zhipu, Kluster, GLHF, Hyperbolic |
| **积分 / 低价** | Together AI, OpenRouter, Fireworks, DeepSeek, DeepInfra, Perplexity, AI21, Upstage, Lepton, Novita, Nebius, Chutes, Replicate, Alibaba, Moonshot, Yi, Baichuan |
| **高级** | OpenAI, Azure OpenAI, Anthropic Claude, Reka AI |

---

## 开始使用（完全零基础指南）

> **完全不需要编程经验。** 按步骤逐一操作即可。

### 第1步：安装Python

1. 访问 [python.org/downloads](https://www.python.org/downloads/)
2. 点击黄色大按钮 **"Download Python"**
3. 运行下载的文件
4. **重要：** 勾选底部的 **"Add Python to PATH"**！
5. 点击 **"Install Now"**

**验证：** 打开命令提示符（`Win + R` > 输入 `cmd` > 回车）：
```
python --version
```
看到 `Python 3.13.x` 类似输出即可。

### 第2步：下载项目

**方法A：使用Git（推荐）**
```
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**方法B：直接下载**
1. 访问 [GitHub页面](https://github.com/sodam-ai/ai-news-radar)
2. 点击绿色 **"Code"** 按钮 > **"Download ZIP"**
3. 解压ZIP文件

### 第3步：安装依赖包

在项目文件夹中打开命令提示符：
```
pip install -r requirements.txt
```
14个包会自动安装。等待安装完成。

### 第4步：获取免费API密钥

**推荐Groq（最简单）：**
1. 访问 [console.groq.com/keys](https://console.groq.com/keys)
2. 用Google账号注册
3. 点击 **"Create API Key"**
4. 复制密钥（以 `gsk_` 开头）

### 第5步：设置API密钥

1. 在项目文件夹找到 `.env.example` 文件
2. 复制并重命名为 `.env`
3. 用记事本打开 `.env`
4. 输入密钥：
```
GROQ_API_KEY=gsk_在此输入你的密钥
```
5. 保存并关闭

> **安全提示：** `.env` 文件会被自动排除在GitHub之外，请勿分享此文件。

### 第6步：启动应用

**Web模式（浏览器）：**
```
streamlit run app.py
```
浏览器自动打开 **http://localhost:6601**

**桌面模式（原生窗口）：**
```
python desktop.py
```
或双击 `AI_News_Radar.bat`

### 第7步：首次使用

1. 点击侧边栏 **"收集"** → 从74个来源收集新闻
2. 点击 **"AI处理"** → AI分析所有文章
3. 点击 **"生成简报"** → 创建今日TOP 5
4. 在仪表板中自由探索！

---

## 使用指南

| 想要做什么 | 方法 |
|-----------|------|
| 看今日摘要 | Dashboard标签 > 简报 |
| 只看图像/视频新闻 | Dashboard标签 > 选择分类 |
| 搜索特定主题 | News Feed标签 > 搜索视图 > 输入关键词 |
| 向AI提问 | AI标签 > 聊天 > 输入问题 |
| 对比AI工具 | Insights标签 > 工具对比 |
| 查看趋势 | Insights标签 > 趋势 |
| 生成社交内容 | Share标签 > 内容生成 > 选择文章+平台 |
| 发布到社交平台 | Share标签 > 社交发布 > 选择平台 > 发布 |
| 语音收听 | Dashboard标签 > 选择语音 > 点击"语音" |
| 导出PDF | Share标签 > 导出 |
| 保存文章 | News Feed标签 > 点击文章的☆ |
| 追踪关键词 | 侧边栏 > 监控列表 > 输入关键词 |

---

## 项目结构

```
ai-news-radar/          （来源74个 / 模块24个 / 提交36个）
├── app.py                    # 主仪表板（5个标签页）
├── desktop.py                # 桌面应用（pywebview + 托盘）
├── config.py                 # 配置（9分类，3情感）
├── requirements.txt          # 14个包
├── ai/                       # AI模块组
│   ├── model_router.py       #   35个LLM提供商
│   ├── briefing.py           #   每日+领域简报
│   ├── chat.py               #   AI新闻聊天
│   ├── voice_briefing.py     #   TTS语音（edge-tts）
│   ├── factcheck.py          #   多源交叉验证
│   ├── glossary.py           #   AI术语表
│   ├── weekly_report.py      #   周度情报报告
│   ├── competitor.py         #   19工具监控
│   ├── trend.py              #   关键词趋势分析
│   ├── debate.py             #   AI辩论
│   └── smart_alert.py        #   桌面通知
├── sns/                      # 社交模块
│   ├── card_generator.py     #   卡片新闻图片（Pillow）
│   ├── poster.py             #   5平台适配器
│   ├── content_generator.py  #   AI内容（5种）
│   └── newsletter.py         #   邮件通讯（SMTP）
├── bot/telegram_bot.py       # Telegram机器人（7个命令）
├── scripts/                  # CLI工具
├── .github/workflows/        # GitHub Actions（每天3次）
├── crawler/                  # RSS收集（并行爬取）
├── reader/                   # 无广告文章阅读器
├── export/                   # Markdown + PDF导出
├── data/                     # 74个预设来源
└── PRD/                      # 设计文档
```

---

## 故障排除

| 问题 | 解决方法 |
|------|----------|
| 找不到 `pip` | 重装Python时勾选"Add to PATH" |
| 找不到 `streamlit` | 运行：`pip install streamlit` |
| "API密钥未设置"警告 | 在 `.env` 文件中填入API密钥 |
| 没有文章显示 | 先点"收集"，再点"AI处理" |
| 分类过滤显示0条 | 运行 `python scripts/reclassify.py` 重新分类 |
| 端口被占用 | 使用 `streamlit run app.py --server.port 7429` |
| PDF导出失败 | 仅Windows支持（使用韩文字体） |

---

## 路线图

| Phase | 功能 | 状态 |
|-------|------|------|
| Phase 1 | 收集+AI摘要+仪表板（17项） | **已完成** |
| Phase 2-A | 搜索+收藏+情感分析+聊天（5项） | **已完成** |
| Phase 2-B | 语音+Telegram+事实核查+术语表+Actions（5项） | **已完成** |
| Tier 1 | 领域简报+周报+工具对比（3项） | **已完成** |
| Tier 2 | 趋势图表+AI辩论（2项） | **已完成** |
| S-Tier | 智能提醒+内容生成+邮件通讯+社交发布（4项） | **已完成** |
| UI/UX | 5标签页重设计+分页+高级CSS | **已完成** |
| Desktop | pywebview+系统托盘+通知 | **已完成** |
| Next | 自动翻译、ChromaDB、Ollama、游戏化 | 计划中 |

---

## 技术栈

| 组件 | 技术 |
|------|------|
| 语言 | Python 3.11+ |
| 仪表板 | Streamlit |
| AI | 35个LLM平台 |
| 图表 | Plotly |
| 语音 | edge-tts（Microsoft TTS） |
| 图片 | Pillow（卡片新闻） |
| 桌面 | pywebview + pystray |
| 机器人 | python-telegram-bot |
| 社交 | tweepy (X), Telegram API, Discord Webhook, Threads API, Instagram Graph API |
| CI/CD | GitHub Actions |
| 数据 | 本地JSON |

---

## 许可证

MIT License - Copyright (c) 2026 **SoDam AI Studio**

详情请参阅 [LICENSE](./LICENSE)。

---

*使用 Streamlit + 35个AI平台构建 — SoDam AI Studio*
