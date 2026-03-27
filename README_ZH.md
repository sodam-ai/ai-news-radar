<div align="center">

# AI News Radar

**AI驱动的新闻智能平台 — 自动收集、分析和推送来自74个来源的AI新闻，支持35个LLM**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.44+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![LLMs](https://img.shields.io/badge/LLM平台-35个-blueviolet)](#35个llm平台)
[![Sources](https://img.shields.io/badge/新闻来源-74个-blue)](#74个新闻来源)
[![Commits](https://img.shields.io/badge/提交-37个-orange)](#)
[![License](https://img.shields.io/badge/许可证-MIT-green)](./LICENSE)

**[English](./README.md) / [Korean](./README_KO.md) / [Japanese](./README_JA.md) / Chinese**

</div>

---

## 这是什么？

AI领域每小时都在变化。新模型发布、工具更新、论文发表、公司动态——全都散落在数十个不同的网站上。**AI News Radar** 消除这些噪音。它持续从**74个精选来源**收集新闻，用AI对每篇文章进行摘要、分类、重要性评分和事实核查，然后以清晰、可操作的简报形式呈现——使用您的语言，按您的时间表，在您偏好的平台上。

**一句话总结：** 不再需要访问74个网站。让AI全部读完，只告诉你重要的内容。

---

## 核心特点

- **50+功能** — 5个标签页（仪表板 / 新闻feed / AI / 洞察 / 分享）
- **74个来源** — 通用AI(26) + 图片·视频(20) + Vibe编程(19) + 本体论(9)
- **35个LLM平台** — 大多数有免费额度，只需一个API密钥
- **9个类别** — 工具、研究、趋势、教程、商业、图片·视频、Vibe编程、本体论、其他
- **追踪19个AI工具** — 自动检测版本发布
- **5个社交平台** — X、Telegram、Discord、Threads、Instagram + 自动生成卡片新闻
- **5种内容类型** — 推文、线程、Instagram说明、博客文章、LinkedIn帖子
- **语音简报**、AI事实核查、AI术语词典、AI辩论
- **一键全流水线** — 收集 > 分析 > 简报 > 发布检测
- **桌面应用** — 系统托盘 + 后台通知
- **GitHub Actions** — 每天自动收集3次
- **自动韩语翻译**（英语 → 韩语）

---

## 主要功能（50+）

### 仪表板标签页

| 功能 | 说明 |
|------|------|
| 每日简报 | AI生成的"今日AI新闻TOP5"（含重要性排名） |
| 专题简报 | 图片·视频 / Vibe编程 / 本体论专属简报 |
| 分类快速筛选 | 9个类别一键筛选 |
| 情感仪表盘 | 正面/中性/负面比例的Plotly交互式图表 |
| 语音简报 | 通过edge-tts以AI语音收听简报 |
| 每周智能报告 | 包含趋势、预测和分析的自动生成周报 |
| 新闻通讯 | 通过SMTP发送日报/周报邮件 |

### 新闻Feed标签页

| 功能 | 说明 |
|------|------|
| 74来源收集 | 15个并行工作器快速聚合 |
| AI摘要 | 每篇文章的3行韩语摘要 |
| 9类别分类 | AI自动分类 |
| 重要性评分 | 每篇文章1–5星评级 |
| 情感分析 | 正面/中性/负面标签 |
| AI事实核查 | 跨来源验证（"3家媒体确认" vs "单一来源"） |
| 重复文章合并 | 多家媒体的同一新闻自动合并 |
| 关键词监控列表 | 追踪关键词高亮显示和提醒 |
| 应用内阅读器 | 在仪表板内阅读完整文章（无广告） |
| 高级搜索 | 按关键词、类别、情感、阅读状态筛选 |
| 书签 + 备忘 | 带个人备注保存文章 |
| 分页 | 每页10篇文章，流畅导航 |
| 时间线视图 | 按今天/昨天/本周浏览 |
| 自动韩语翻译 | 英文文章自动翻译为韩语 |

### AI标签页

| 功能 | 说明 |
|------|------|
| AI新闻聊天 | 用自然语言询问收集到的新闻 |
| AI术语词典 | 自动提取的AI术语 + 初学者友好解释 |

### 洞察标签页

| 功能 | 说明 |
|------|------|
| AI工具发布追踪器 | 追踪19个AI工具，自动检测发布 |
| 趋势图表 | 每日提及频率的Plotly折线图 |
| 热门关键词 | 环比上升的关键词 |
| AI辩论 | "Midjourney vs Flux" — AI生成优缺点和结论 |
| 每周智能报告 | 深度周度分析与预测 |

### 分享标签页

| 功能 | 说明 |
|------|------|
| SNS自动发布 | 发布到X、Telegram、Discord、Threads和Instagram |
| 卡片新闻生成器 | 自动生成1080×1080卡片图片（深色主题，按类别配色） |
| AI内容生成 | 自动生成推文、线程、Instagram说明、博客文章、LinkedIn帖子 |
| 新闻通讯邮件 | 向订阅者列表发送格式化简报 |
| 导出 | 下载为Markdown或PDF |

### 系统功能

| 功能 | 说明 |
|------|------|
| 一键全流水线 | 收集 > AI处理 > 简报 > 发布检测，一键完成 |
| 并行爬取 | 15个并发工作器快速收集 |
| 批量并行处理 | 大量文章的高效AI批量处理 |
| 智能关键词提醒 | 监控关键词出现时桌面通知 |
| 桌面应用 | pywebview原生窗口 + 系统托盘 + 后台模式 |
| GitHub Actions | 每天自动收集3次（可配置） |
| Telegram机器人 | 7个命令随时随地访问 |

---

## 74个新闻来源

| 类别 | 数量 | 示例 |
|------|:----:|------|
| **通用AI** | 26 | TechCrunch, The Verge, MIT Tech Review, Wired, ZDNET, Ben's Bites, Ars Technica |
| **图片·视频** | 20 | Stability AI, Civitai, Runway, Reddit (StableDiffusion, midjourney, flux_ai, comfyui) |
| **Vibe编程** | 19 | Cursor, GitHub, Anthropic, Simon Willison, Reddit (vibecoding, ClaudeAI, cursor) |
| **本体论** | 9 | Neo4j, Stardog, W3C, Reddit (semanticweb, KnowledgeGraphs) |

---

## 35个LLM平台

只需从以下平台获取**一个API密钥**即可：

| 等级 | 平台 |
|------|------|
| **免费（推荐）** | Gemini, Groq, Cerebras, SambaNova, xAI, Mistral, Cohere, HuggingFace, NVIDIA, Cloudflare, Zhipu, Kluster, GLHF, Hyperbolic |
| **点数/低价** | Together AI, OpenRouter, Fireworks, DeepSeek, DeepInfra, Perplexity, AI21, Upstage, Lepton, Novita, Nebius, Chutes, Replicate, Alibaba, Moonshot, Yi, Baichuan |
| **高级** | OpenAI, Azure OpenAI, Anthropic Claude, Reka AI |

> **提示：** Gemini和Groq免费额度充足，设置最简单。

---

## 仪表板概览（5个标签页）

| 标签页 | 内容 |
|--------|------|
| **仪表板** | 每日简报、专题简报、分类快速筛选、情感图表、周报、新闻通讯 |
| **新闻Feed** | 全部新闻、高级搜索、书签、时间线视图、分页 |
| **AI** | 新闻聊天、AI术语词典 |
| **洞察** | 发布追踪器、趋势图表、热门关键词、AI辩论、周报 |
| **分享** | SNS发布、AI内容生成、卡片新闻、新闻通讯、导出 |

---

## 快速上手 — 7步入门指南

> **完全不需要编程经验。** 请仔细按照每个步骤操作。

### 第1步 — 安装Python

1. 访问 [python.org/downloads](https://www.python.org/downloads/)
2. 点击大黄色 **"Download Python"** 按钮
3. 运行下载的文件
4. **关键：** 安装界面底部的 **"Add Python to PATH"** 复选框**必须勾选**
5. 点击 **"Install Now"**

**验证安装：** 打开终端（`Win + R` → 输入 `cmd` → Enter）并运行：

```bash
python --version
```

看到 `Python 3.11.x` 或更高版本即为成功。

### 第2步 — 下载项目

**方法A：使用Git（推荐）**

```bash
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**方法B：直接下载**

1. 访问 [GitHub仓库](https://github.com/sodam-ai/ai-news-radar)
2. 点击绿色 **"Code"** 按钮 → **"Download ZIP"**
3. 将ZIP解压到您选择的文件夹
4. 在该文件夹中打开终端

### 第3步 — 创建虚拟环境（推荐）

```bash
python -m venv venv
```

激活：

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

终端开头出现 `(venv)` 即为成功。

### 第4步 — 安装依赖

```bash
pip install -r requirements.txt
```

这将安装所有必需的包。可能需要1–2分钟。

### 第5步 — 获取免费API密钥

**从以下平台选择任意一个。** 推荐 **Groq** 设置最快：

1. 访问 [console.groq.com/keys](https://console.groq.com/keys)
2. 用Google账号注册（10秒）
3. 点击 **"Create API Key"**
4. 复制密钥（以 `gsk_` 开头）

> 其他免费选项：[Gemini](https://aistudio.google.com/apikey)，[Cerebras](https://cloud.cerebras.ai/)，[SambaNova](https://cloud.sambanova.ai/)

### 第6步 — 配置API密钥

1. 在项目文件夹中找到 `.env.example` 文件
2. 复制并将其重命名为 `.env`
3. 用任意文本编辑器（记事本即可）打开 `.env`
4. 粘贴您的API密钥：

```env
# 选择一个或多个：
GROQ_API_KEY=gsk_将您的实际密钥粘贴在这里
# GEMINI_API_KEY=your_gemini_key
# OPENAI_API_KEY=sk-your_openai_key
```

5. 保存并关闭文件

> **安全提示：** `.env` 文件已列入 `.gitignore`，永远不会上传到GitHub。请勿公开分享此文件。

### 第7步 — 启动应用

**网页模式（在浏览器中打开）：**

```bash
streamlit run app.py
```

浏览器自动打开 **http://localhost:6601**

**桌面模式（原生窗口）：**

```bash
python desktop.py
```

或在Windows上双击 **`AI_News_Radar.bat`**。

### 首次使用

1. 点击侧边栏的 **"收集"** — 从74个来源收集新闻（约1分钟）
2. 点击 **"AI处理"** — AI分析、摘要和分类所有文章
3. 点击 **"生成简报"** — 生成今日TOP5简报
4. 探索5个标签页，发现所有功能！

---

## 使用指南

| 您想要做什么 | 如何操作 |
|------------|---------|
| 阅读今日摘要 | 仪表板标签页 > 简报部分 |
| 按类别筛选 | 仪表板标签页 > 点击任意分类快速筛选 |
| 搜索特定话题 | 新闻Feed标签页 > 搜索视图 > 输入关键词 |
| 向AI提问新闻 | AI标签页 > 聊天视图 > 输入问题 |
| 学习AI术语 | AI标签页 > 词典视图 > 浏览或搜索 |
| 追踪AI工具发布 | 洞察标签页 > 发布追踪器 |
| 查看热门关键词 | 洞察标签页 > 趋势 |
| 运行AI辩论 | 洞察标签页 > AI辩论 > 选择两个工具 |
| 生成社交媒体内容 | 分享标签页 > 内容生成 > 选择文章+平台 |
| 发布到社交媒体 | 分享标签页 > SNS发布 > 选择平台 > 发布 |
| 收听语音简报 | 仪表板标签页 > 选择声音 > 点击"语音" |
| 导出为PDF | 分享标签页 > 导出视图 |
| 保存文章 | 新闻Feed标签页 > 点击任意文章的书签图标 |
| 设置关键词提醒 | 侧边栏 > 监控列表 > 输入关键词 |
| 运行完整流水线 | 侧边栏 > "一键流水线" 按钮 |

---

## 社交平台设置

| 平台 | 设置时间 | 难度 | 指南 |
|------|:-------:|:----:|------|
| Discord | 30秒 | 非常简单 | 在频道设置中创建Webhook URL |
| Telegram | 2分钟 | 简单 | 通过@BotFather创建机器人 |
| X (Twitter) | 10分钟 | 中等 | 申请开发者账号 |
| Threads | 10分钟 | 中等 | Meta开发者门户 |
| Instagram | 15分钟 | 复杂 | Instagram Graph API设置 |

详细的分步说明可在应用内 **分享标签页 > SNS发布** 部分找到。

---

## 项目结构

```
ai-news-radar/
├── app.py                       # 主仪表板（5个标签页）
├── desktop.py                   # 桌面应用（pywebview + 系统托盘）
├── config.py                    # 设置（9个类别、端口、路径）
├── requirements.txt             # 必需包列表
├── .env.example                 # API密钥模板
├── AI_News_Radar.bat            # Windows启动器（网页模式）
├── AI_News_Radar_Silent.vbs     # 静默启动器（无控制台窗口）
│
├── ai/                          # 14个AI模块
│   ├── model_router.py          #   35个LLM提供商路由
│   ├── briefing.py              #   每日+专题简报生成
│   ├── chat.py                  #   自然语言新闻聊天
│   ├── voice_briefing.py        #   TTS语音输出（edge-tts）
│   ├── factcheck.py             #   跨来源事实验证
│   ├── glossary.py              #   AI术语词典
│   ├── weekly_report.py         #   每周智能报告
│   ├── competitor.py            #   AI工具发布监控
│   ├── release_tracker.py       #   自动发布检测
│   ├── trend.py                 #   关键词趋势分析
│   ├── debate.py                #   AI辩论模式
│   ├── smart_alert.py           #   桌面关键词通知
│   ├── translator.py            #   韩语自动翻译
│   ├── deduplicator.py          #   重复文章合并
│   └── batch_processor.py       #   批量并行处理
│
├── sns/                         # SNS·分享模块
│   ├── card_generator.py        #   1080×1080卡片新闻图片（Pillow）
│   ├── poster.py                #   5平台SNS发布
│   ├── content_generator.py     #   AI内容（5种类型）
│   └── newsletter.py            #   邮件新闻通讯（SMTP）
│
├── crawler/                     # 数据收集
│   ├── rss_crawler.py           #   RSS爬虫（15个并行工作器）
│   └── scheduler.py             #   APScheduler定时任务
│
├── bot/                         # Telegram集成
│   └── telegram_bot.py          #   Telegram机器人（7个命令）
│
├── reader/                      # 文章阅读
│   └── article_reader.py        #   应用内文章阅读器（无广告）
│
├── export/                      # 数据导出
│   └── exporter.py              #   Markdown + PDF导出
│
├── utils/                       # 共享工具
│   └── helpers.py               #   通用辅助函数
│
├── scripts/                     # CLI工具
│   ├── collect.py               #   独立收集脚本
│   └── reclassify.py            #   类别重分类工具
│
├── data/                        # 本地数据存储
│   ├── preset_sources.json      #   74个来源定义
│   ├── sources.json             #   活跃来源配置
│   ├── articles.json            #   收集的文章
│   ├── briefings.json           #   生成的简报
│   ├── weekly_reports.json      #   周报归档
│   ├── release_log.json         #   工具发布历史
│   ├── audio/                   #   语音简报音频文件
│   └── cards/                   #   生成的卡片新闻图片
│
├── .github/workflows/
│   └── collect.yml              #   GitHub Actions（每天自动收集3次）
│
└── PRD/                         #   产品设计文档
```

**8个目录，24个模块** — **37次提交**，持续更新中。

---

## 技术栈

| 组件 | 技术 |
|------|------|
| **语言** | Python 3.11+ |
| **仪表板** | Streamlit 1.44+ |
| **AI引擎** | 统一模型路由器接入35个LLM平台 |
| **图表** | Plotly（交互式趋势图表、情感仪表盘） |
| **语音** | edge-tts（微软神经网络TTS） |
| **图片生成** | Pillow（深色主题卡片新闻） |
| **桌面** | pywebview + pystray（原生窗口 + 系统托盘） |
| **通知** | plyer（跨平台桌面提醒） |
| **RSS解析** | feedparser（74个来源订阅） |
| **网页爬虫** | BeautifulSoup4 + requests |
| **Telegram机器人** | python-telegram-bot |
| **SNS API** | tweepy (X), Telegram API, Discord Webhook, Threads API, Instagram Graph API |
| **邮件** | smtplib（SMTP新闻通讯） |
| **PDF导出** | fpdf2（支持韩语字体） |
| **定时任务** | APScheduler（应用内）、GitHub Actions（CI/CD） |
| **数据存储** | 本地JSON（无需数据库配置） |

---

## 故障排除

| 问题 | 解决方法 |
|------|---------|
| 找不到 `python` 命令 | 勾选 **"Add to PATH"** 重新安装Python |
| 找不到 `pip` 命令 | 改用 `python -m pip install -r requirements.txt` |
| 找不到 `streamlit` | 运行 `pip install streamlit`，检查虚拟环境是否激活 |
| "未设置API密钥" 警告 | 在 `.env` 文件中输入至少一个API密钥（参见第6步） |
| 没有文章显示 | 先点击 **"收集"**，再点击 **"AI处理"** |
| 类别显示0篇文章 | 运行 `python scripts/reclassify.py` 重新分类 |
| 端口6601已被占用 | 使用 `streamlit run app.py --server.port 7777` |
| macOS/Linux上PDF导出失败 | 安装 `NanumGothic` 字体 |
| 桌面模式无法启动 | 确认已安装 `pip install pywebview` |
| 收集速度慢 | 正常现象 — 74个来源15个并行工作器约需60秒 |
| edge-tts语音错误 | 检查网络连接（edge-tts需要在线使用） |

---

## 路线图

| 阶段 | 功能 | 状态 |
|------|------|:----:|
| **Phase 1** | 收集 + AI摘要 + 仪表板（17项功能） | ✅ 完成 |
| **Phase 2-A** | 搜索 + 书签 + 情感 + 聊天（5项功能） | ✅ 完成 |
| **Phase 2-B** | 语音 + Telegram + 事实核查 + 词典 + Actions（5项功能） | ✅ 完成 |
| **Tier 1** | 专题简报 + 周报 + 发布追踪器（3项功能） | ✅ 完成 |
| **Tier 2** | 趋势图表 + AI辩论 + 热门关键词（3项功能） | ✅ 完成 |
| **S级** | 智能提醒 + 内容生成 + 新闻通讯 + SNS（4项功能） | ✅ 完成 |
| **UI/UX** | 5标签页重设计 + 分页 + 分类快速筛选 + 高级CSS | ✅ 完成 |
| **桌面** | pywebview + 系统托盘 + 后台通知 | ✅ 完成 |
| **流水线** | 一键全流水线 + 并行爬取 + 批量处理 | ✅ 完成 |
| **翻译** | 韩语自动翻译 + 去重 | ✅ 完成 |
| **下一步** | ChromaDB向量搜索、Ollama本地LLM、游戏化、移动PWA | 📋 计划中 |

---

## 贡献

欢迎提交Pull Request！

1. Fork本仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 开启Pull Request

---

## 许可证

MIT许可证 — Copyright (c) 2026 **SoDam AI Studio**

详情请参阅 [LICENSE](./LICENSE)。

---

<div align="center">

*由 Streamlit + 35个AI平台构建 — SoDam AI Studio*

</div>
