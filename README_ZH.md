<div align="center">

# AI News Radar

**AI驱动的新闻情报平台 -- 从74个来源自动采集、分析、生成简报，支持35个LLM平台。**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.44+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![LLMs](https://img.shields.io/badge/LLM平台-35个-blueviolet)](#35个llm平台)
[![Sources](https://img.shields.io/badge/新闻来源-74个-blue)](#74个新闻来源)
[![License](https://img.shields.io/badge/License-SoDam_AI_Studio-green)](./LICENSE)

**[English](./README.md) &nbsp;/&nbsp; [한국어](./README_KO.md) &nbsp;/&nbsp; [日本語](./README_JA.md) &nbsp;/&nbsp; 中文**

</div>

---

## 什么是 AI News Radar?

AI领域每小时都在变化。新模型发布、工具更新、论文发表、企业动向 -- 所有信息散落在几十个不同的网站上。**AI News Radar** 帮你消除这些噪音。它从**74个精选来源**持续采集新闻，由AI自动完成摘要、分类、重要性评分和事实核查，最终以简洁实用的简报形式呈现给你。

**一句话概括：** 不用再逐个浏览74个网站了。让AI全部读完，只告诉你最重要的内容。

---

## 安全与隐私 -- 请先阅读

### 你的 API 密钥 100% 私有 -- 绝不会被上传

下载本项目时，**不包含任何 API 密钥、密码或个人数据。**

工作原理：
- 你在自己的电脑上创建一个名为 `.env` 的文件
- 将你自己申请的 API 密钥填入该文件（可从 Google/Groq 等平台免费获取）
- 该文件**绝不会离开你的电脑** -- `.gitignore` 会阻止它被上传
- 每个下载此应用的人都使用**自己的密钥**和**自己的配额**

### 安全证明

| 检查项 | 结果 |
|--------|------|
| GitHub 仓库中是否存在 `.env` 文件 | 不存在（已被 .gitignore 屏蔽） |
| 源代码中是否硬编码 API 密钥 | 没有 -- 所有代码都从环境变量中读取 |
| 你的密钥是否会被他人共享 | 不可能 -- 每个用户各自设置自己的密钥 |
| 应用是否连接 AI 服务商以外的服务器 | 不会 -- 只连接新闻 RSS 源和你选择的 AI API |

### 每位用户需要做的事

每个下载此应用的人需要：
1. 自行获取一个免费 API 密钥（10秒即可完成，无需信用卡）
2. 创建自己的 `.env` 文件并填入密钥
3. 完成 -- 你使用你的配额，我使用我的配额，完全独立

---

## 功能分类 -- 哪些需要 API 密钥

### 立即可用 -- 无需 API 密钥

下载并运行后即可使用的功能：

| 功能 | 实现方式 |
|------|----------|
| **从74个来源采集新闻** | RSS 源读取（仅需联网） |
| **文章列表与浏览** | 本地文件读取 |
| **书签与阅读记录** | 保存在本地电脑 |
| **高级搜索与筛选** | 本地数据处理 |
| **导出（PDF / Markdown）** | 本地文件生成 |
| **应用内文章阅读器** | 网页抓取 |
| **时间线浏览** | 本地数据展示 |

### 需要 API 密钥（有免费选项）

以下功能使用 AI -- 需要一个免费 API 密钥：

| 功能 | 为何需要 API 密钥 |
|------|-------------------|
| **AI 新闻分类** | AI 阅读并分类每篇文章 |
| **三行摘要** | AI 为每篇文章生成摘要 |
| **每日简报（TOP 5）** | AI 筛选并解读重要新闻 |
| **英文翻译为韩文** | AI 翻译文章内容 |
| **AI 新闻聊天机器人** | AI 回答你关于新闻的问题 |
| **事实核查** | AI 交叉验证多个来源 |
| **AI 辩论** | AI 生成两个工具的优缺点对比 |
| **AI 术语词典** | AI 解释专业术语 |
| **周报** | AI 生成每周分析报告 |
| **一键全流程** | 一次运行所有 AI 功能 |

> **免费的 Gemini API 密钥**（来自 Google）每天允许 1,000 次 AI 调用 -- 个人日常使用完全够用。

---

## 主要特点

- **50+ 项功能** -- 5个标签页
- **74个来源** -- 通用 AI (26) + 图像/视频 (20) + Vibe Coding (19) + 本体论 (9)
- **35个 LLM 平台** -- 大多数有免费套餐，只需一个 API 密钥
- **9个分类** -- 工具、研究、趋势、教程、商业、图像/视频、Vibe Coding、本体论、其他
- **19个 AI 工具**自动版本发布检测
- **5个 SNS 平台** -- X、Telegram、Discord、Threads、Instagram + 自动卡片新闻生成
- **语音简报**、AI 事实核查、AI 术语词典、AI 辩论
- **一键全流程** -- 采集 > 分析 > 简报 > 发布检测
- **桌面应用** -- 系统托盘 + 后台通知
- **GitHub Actions** -- 每天自动采集3次

---

## 功能列表（50+）

### 仪表板标签页

| 功能 | 说明 |
|------|------|
| 每日简报 | AI 生成"今日 AI 新闻 TOP 5"（按重要性排列） |
| 专题简报 | 图像/视频、Vibe Coding、本体论专属简报 |
| 分类快捷筛选 | 9个分类一键筛选 |
| 情感仪表盘 | 正面/中性/负面比例的 Plotly 交互式图表 |
| 语音简报 | 通过 edge-tts 收听 AI 语音简报 |
| 周报 | 包含趋势、预测、分析的自动生成周报 |
| 邮件订阅 | 通过 SMTP 发送每日/每周简报邮件 |

### 新闻源标签页

| 功能 | 说明 |
|------|------|
| 74来源采集 | 15个并行工作线程快速采集 |
| AI 摘要 | 每篇文章三行摘要 |
| 9分类自动归类 | AI 自动分类 |
| 重要性评分 | 每篇文章1~5分评级 |
| 情感分析 | 正面/中性/负面标签 |
| AI 事实核查 | 多来源交叉验证 |
| 重复合并 | 同一新闻多来源自动合并 |
| 关键词监控列表 | 追踪关键词高亮显示及提醒 |
| 应用内阅读器 | 无广告应用内全文阅读 |
| 高级搜索 | 按关键词、分类、情感、已读状态筛选 |
| 书签 + 备注 | 带个人备注保存文章 |
| 分页 | 每页10篇文章 |
| 时间线浏览 | 今天 / 昨天 / 本周 |
| 自动翻译 | 英文文章自动翻译为韩文 |

### AI 标签页

| 功能 | 说明 |
|------|------|
| AI 新闻聊天 | 用自然语言询问已采集的新闻 |
| AI 术语词典 | 自动提取 AI 术语，附带通俗易懂的解释 |

### 洞察标签页

| 功能 | 说明 |
|------|------|
| AI 工具发布追踪器 | 追踪19个 AI 工具的版本发布 |
| 趋势图表 | Plotly 交互式每日提及频率折线图 |
| 热门关键词 | 按周环比上升率排列的关键词 |
| AI 辩论 | AI 生成两个工具的优缺点及结论 |
| 周报 | 包含预测的深度每周分析 |

### 分享标签页

| 功能 | 说明 |
|------|------|
| SNS 自动发布 | 发布到 X、Telegram、Discord、Threads、Instagram |
| 卡片新闻生成器 | 自动生成 1080x1080 暗色主题卡片图片 |
| AI 内容生成 | 自动生成推文、帖子串、Instagram 描述、博客文章、LinkedIn 帖子 |
| 邮件简报 | 向订阅者发送格式化简报 |
| 导出 | 下载为 Markdown 或 PDF |

### 系统功能

| 功能 | 说明 |
|------|------|
| 一键全流程 | 采集 > AI 处理 > 简报 > 发布检测，一键完成 |
| 并行采集 | 15个并发工作线程快速采集 |
| 智能关键词提醒 | 监控关键词出现时推送桌面通知 |
| 桌面应用 | pywebview 原生窗口 + 系统托盘 + 后台运行 |
| GitHub Actions | 每天自动采集3次（可配置） |
| Telegram 机器人 | 7个指令，随时随地访问 |

---

## 74个新闻来源

| 分类 | 数量 | 示例 |
|------|:----:|------|
| **通用 AI** | 26 | TechCrunch, The Verge, MIT Tech Review, Wired, ZDNET, Ben's Bites, Ars Technica |
| **图像/视频** | 20 | Stability AI, Civitai, Runway, Reddit (StableDiffusion, midjourney, flux_ai, comfyui) |
| **Vibe Coding** | 19 | Cursor, GitHub, Anthropic, Simon Willison, Reddit (vibecoding, ClaudeAI, cursor) |
| **本体论** | 9 | Neo4j, Stardog, W3C, Reddit (semanticweb, KnowledgeGraphs) |

---

## 35个 LLM 平台

只需从以下平台获取**一个 API 密钥**即可：

| 级别 | 平台 |
|------|------|
| **免费（推荐）** | Gemini, Groq, Cerebras, SambaNova, xAI, Mistral, Cohere, HuggingFace, NVIDIA, Cloudflare, Zhipu, Kluster, GLHF, Hyperbolic |
| **按量计费 / 低价** | Together AI, OpenRouter, Fireworks, DeepSeek, DeepInfra, Perplexity, AI21, Upstage, Lepton, Novita, Nebius, Chutes, Replicate, Alibaba, Moonshot, Yi, Baichuan |
| **高级** | OpenAI, Azure OpenAI, Anthropic Claude, Reka AI |

> **新手推荐：** Gemini（每天 1,000 次免费调用）和 Groq（每天 14,400 次免费调用）-- 无需信用卡。
>
> - **Google Gemini:** [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
> - **Groq:** [console.groq.com/keys](https://console.groq.com/keys)

---

## 仪表板构成（5个标签页）

| 标签页 | 内容 |
|--------|------|
| **仪表板** | 每日简报、专题简报、分类快捷筛选、情感图表、周报、邮件订阅 |
| **新闻源** | 全部新闻、高级搜索、书签、时间线浏览、分页 |
| **AI** | 新闻聊天、AI 术语词典 |
| **洞察** | 发布追踪器、趋势图表、热门关键词、AI 辩论、周报 |
| **分享** | SNS 发布、AI 内容生成、卡片新闻、邮件简报、导出 |

---

## 快速入门 -- 零基础完整指南（分步操作）

> **完全不需要编程经验。** 只要你会复制粘贴，就能完成设置。请逐步操作。

---

### 第1步 -- 安装 Python

Python 是运行本应用所需的编程语言，只需安装一次。

**操作步骤：**

1. 打开浏览器，访问 **https://www.python.org/downloads/**
2. 点击页面中央黄色的 **"Download Python"** 按钮
3. 下载完成后，双击运行下载的 `.exe` 文件
4. **【极其重要】** 安装界面底部有一个 **"Add Python to PATH"** 复选框，**务必勾选**。忘记勾选会导致后续步骤报错。
5. 点击 **"Install Now"** 并等待安装完成（约1-2分钟）

**验证安装是否成功：**

同时按下 `Win + R` 键，在弹出的窗口中输入 `cmd` 并按回车。在黑色窗口中输入：

```bash
python --version
```

如果看到类似 `Python 3.11.9` 的输出，说明安装成功。如果报错，请重新安装 Python 并确保勾选了"Add Python to PATH"。

---

### 第2步 -- 下载项目

**方式A：直接下载（最简单）**

1. 访问 **https://github.com/sodam-ai/ai-news-radar**
2. 点击右上角绿色的 **"Code"** 按钮
3. 点击 **"Download ZIP"**
4. 找到下载的 ZIP 文件（通常在"下载"文件夹中）
5. 右键点击 > **"全部解压缩"** > 选择目标文件夹 > 点击"解压缩"
6. 解压后会得到一个 `ai-news-radar-main` 文件夹

**方式B：Git 克隆（需要已安装 Git）**

```bash
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

---

### 第3步 -- 打开终端

1. 打开解压后的文件夹（包含 `app.py` 的那个文件夹）
2. 点击文件资源管理器顶部的地址栏
3. 输入 `cmd` 并按回车
4. 黑色终端窗口将在正确的文件夹中打开

---

### 第4步 -- 安装依赖包

在终端窗口中输入以下命令并按回车：

```bash
pip install -r requirements.txt
```

等待完成（约1-3分钟）。屏幕上会滚动大量文本，这是正常现象。

---

### 第5步 -- 获取免费 API 密钥

使用 AI 功能需要一个免费 API 密钥。以下是最快的获取方式：

#### 推荐1：Google Gemini（每天1,000次免费调用）

1. 访问 **https://aistudio.google.com/apikey**
2. 使用 Google 账号登录
3. 点击 **"Create API Key"**
4. 点击 **"Create API key in new project"**
5. 复制生成的密钥（以 `AIzaSy...` 开头）

#### 推荐2：Groq（每天14,400次免费调用，速度更快）

1. 访问 **https://console.groq.com/keys**
2. 使用 Google 账号注册（10秒完成）
3. 点击 **"Create API Key"**
4. 复制密钥（以 `gsk_` 开头）

> **无需信用卡。** 以上任何方式都不会产生费用。

> **其他免费选项：**
> - [Cerebras](https://cloud.cerebras.ai/) -- 超高速免费 API
> - [SambaNova](https://cloud.sambanova.ai/) -- 可免费使用

---

### 第6步 -- 设置 API 密钥

1. 在项目文件夹中找到 **`.env.example`** 文件
   - **如果看不到：** 在文件资源管理器中点击"查看" > 勾选"隐藏的项目"
2. 复制该文件并将副本重命名为 **`.env`**（删除 `.example` 部分）
   - Windows：右键 > 复制 > 粘贴 > 重命名
3. 用记事本打开 `.env`（右键 > 打开方式 > 记事本）
4. 找到对应平台的那行，填入你的密钥：

**如果获取的是 Gemini 密钥：**
```
GEMINI_API_KEY=AIzaSy_在此粘贴你的密钥
```

**如果获取的是 Groq 密钥：**
```
GROQ_API_KEY=gsk_在此粘贴你的密钥
```

5. 保存并关闭文件

> **你的密钥是安全的。** `.env` 文件仅存在于你的电脑上，永远不会上传到 GitHub 或被任何人看到。

---

### 第7步 -- 启动应用

**Web 模式（在浏览器中打开 -- 推荐）：**

```bash
streamlit run app.py
```

浏览器会自动打开 **http://localhost:6601**。如果没有自动打开，请手动在地址栏中输入该地址。

**桌面模式（独立窗口）：**

```bash
python desktop.py
```

**Windows 快捷方式：** 双击项目文件夹中的 **`AI_News_Radar.bat`** 即可启动。

---

### 首次使用 -- 启动后的操作

1. 在左侧边栏点击 **"Collect（采集）"** -- 从74个来源采集新闻（约1分钟）
2. 点击 **"AI Process（AI 处理）"** -- AI 分析所有文章（需要 API 密钥）
3. 点击 **"Briefing（简报）"** -- 生成今日 TOP 5 摘要
4. 浏览5个标签页：仪表板 / 新闻源 / AI / 洞察 / 分享

> **提示：** 即使没有 API 密钥，也可以点击"Collect"采集新闻。文章列表会显示出来，但没有 AI 摘要和分类。之后添加 API 密钥即可解锁所有 AI 功能。

---

## 使用指南

| 你想做什么 | 操作方法 |
|-----------|---------|
| 阅读今日摘要 | 仪表板标签页 > 简报区域 |
| 按分类筛选 | 仪表板标签页 > 点击分类快捷筛选 |
| 搜索特定主题 | 新闻源标签页 > 搜索 > 输入关键词 |
| 向 AI 提问新闻 | AI 标签页 > 聊天 > 输入问题 |
| 学习 AI 术语 | AI 标签页 > 术语词典 > 浏览或搜索 |
| 追踪 AI 工具发布 | 洞察标签页 > 发布追踪器 |
| 查看趋势关键词 | 洞察标签页 > 趋势 |
| 运行 AI 辩论 | 洞察标签页 > AI 辩论 > 选择两个工具 |
| 生成 SNS 内容 | 分享标签页 > 内容生成 |
| 发布到社交媒体 | 分享标签页 > SNS 发布 |
| 收听语音简报 | 仪表板标签页 > 选择语音 > 点击"Voice" |
| 导出为 PDF | 分享标签页 > 导出 |
| 保存文章 | 新闻源标签页 > 点击书签图标 |
| 设置关键词提醒 | 侧边栏 > 监控列表 > 输入关键词 |
| 运行全流程 | 侧边栏 > "一键全流程"按钮 |

---

## SNS 平台设置

| 平台 | 设置时间 | 难度 | 设置方法 |
|------|:--------:|:----:|---------|
| Discord | 30秒 | 非常简单 | 在频道设置中创建 Webhook URL |
| Telegram | 2分钟 | 简单 | 通过 @BotFather 创建机器人 |
| X (Twitter) | 10分钟 | 中等 | 申请开发者账号 |
| Threads | 10分钟 | 中等 | 在 Meta 开发者平台设置 |
| Instagram | 15分钟 | 较复杂 | 配置 Instagram Graph API |

详细的分步说明可在应用内 **分享标签页 > SNS 发布** 区域查看。

---

## 项目结构

```
ai-news-radar/
├── app.py                       # 主仪表板（5个标签页）
├── desktop.py                   # 桌面应用（pywebview + 系统托盘）
├── config.py                    # 配置（9个分类、端口、路径）
├── requirements.txt             # 依赖包列表
├── .env.example                 # API 密钥模板（可安全共享）
├── .env                         # 你的 API 密钥（仅本地存储，不会上传）
├── .gitignore                   # 阻止 .env 被上传
├── AI_News_Radar.bat            # Windows 启动脚本（Web 模式）
├── AI_News_Radar_Silent.vbs     # 静默启动（无控制台窗口）
│
├── ai/                          # AI 模块（14个）
│   ├── model_router.py          #   35个 LLM 提供商路由
│   ├── briefing.py              #   每日 + 专题简报生成
│   ├── chat.py                  #   自然语言新闻聊天
│   ├── voice_briefing.py        #   TTS 语音输出（edge-tts）
│   ├── factcheck.py             #   多来源事实交叉验证
│   ├── glossary.py              #   AI 术语词典
│   ├── weekly_report.py         #   周报
│   ├── release_tracker.py       #   自动版本发布检测
│   ├── trend.py                 #   关键词趋势分析
│   ├── debate.py                #   AI 辩论模式
│   ├── smart_alert.py           #   桌面关键词通知
│   ├── translator.py            #   自动翻译
│   ├── deduplicator.py          #   重复文章合并
│   └── batch_processor.py       #   批量并行处理
│
├── sns/                         # SNS 与分享模块
│   ├── card_generator.py        #   1080x1080 卡片新闻图片
│   ├── poster.py                #   5平台 SNS 发布
│   ├── content_generator.py     #   AI 内容生成（5种类型）
│   └── newsletter.py            #   邮件简报（SMTP）
│
├── crawler/                     # 数据采集
│   ├── rss_crawler.py           #   RSS 爬虫（15个并行工作线程）
│   └── scheduler.py             #   APScheduler 定时调度
│
├── bot/                         # Telegram 集成
│   └── telegram_bot.py          #   Telegram 机器人（7个指令）
│
├── reader/                      # 文章阅读
│   └── article_reader.py        #   无广告应用内文章阅读器
│
├── export/                      # 数据导出
│   └── exporter.py              #   Markdown + PDF 导出
│
├── utils/                       # 公共工具
│   └── helpers.py               #   通用辅助函数
│
├── scripts/                     # CLI 工具
│   ├── collect.py               #   独立采集脚本
│   └── reclassify.py            #   分类重新归类工具
│
├── data/                        # 本地数据存储（不会上传）
│   ├── preset_sources.json      #   74个来源定义
│   ├── articles.json            #   采集的文章
│   ├── briefings.json           #   生成的简报
│   └── ...
│
└── .github/workflows/
    └── collect.yml              #   GitHub Actions（每天自动采集3次）
```

---

## 技术栈

| 组件 | 技术 |
|------|------|
| **编程语言** | Python 3.11+ |
| **仪表板** | Streamlit 1.44+ |
| **AI 引擎** | 通过统一模型路由器接入35个 LLM 平台 |
| **图表** | Plotly（交互式趋势图表、情感仪表盘） |
| **语音** | edge-tts（微软神经网络 TTS） |
| **图片生成** | Pillow（暗色主题卡片新闻） |
| **桌面** | pywebview + pystray（原生窗口 + 系统托盘） |
| **通知** | plyer（跨平台桌面通知） |
| **RSS 解析** | feedparser（74个来源） |
| **网页抓取** | BeautifulSoup4 + requests |
| **Telegram 机器人** | python-telegram-bot |
| **PDF 导出** | fpdf2 |
| **定时调度** | APScheduler + GitHub Actions |
| **数据存储** | 本地 JSON（无需数据库配置） |

---

## 常见问题

| 问题 | 解决方法 |
|------|---------|
| `python` 命令找不到 | 重新安装 Python 并勾选 **"Add to PATH"** |
| `pip` 命令找不到 | 尝试 `python -m pip install -r requirements.txt` |
| `streamlit` 命令找不到 | 运行 `pip install streamlit` |
| "API 密钥未设置"警告 | 创建 `.env` 文件并填入 API 密钥（参见第6步） |
| 没有文章显示 | 先点击"Collect"，等待1分钟，再点击"AI Process" |
| AI 功能不工作 | 确认 `.env` 文件存在且包含有效的 API 密钥 |
| 分类显示0篇文章 | 运行 `python scripts/reclassify.py` |
| 端口6601已被占用 | 使用 `streamlit run app.py --server.port 7777` |
| 采集速度慢 | 正常现象 -- 74个来源约需60秒 |
| `.env` 文件无法创建 | 用记事本新建文件，保存为 `.env`（注意不要保存为 `.env.txt`） |

**API 密钥常见错误：**
- 粘贴密钥时带有多余空格 -- 删除所有空格
- 使用了已过期的密钥 -- 重新生成一个
- 忘记保存 `.env` 文件 -- 确保在记事本中点击了"保存"

---

## 开发路线图

| 阶段 | 功能 | 状态 |
|------|------|:----:|
| **Phase 1** | 采集 + AI 摘要 + 仪表板 | 已完成 |
| **Phase 2** | 搜索 + 书签 + 聊天 + 语音 + 事实核查 | 已完成 |
| **Phase 3** | 洞察 + SNS + 全流程 + 桌面 | 已完成 |
| **下一步** | ChromaDB 向量搜索、Ollama 本地 LLM、移动端 PWA | 规划中 |

---

## 参与贡献

欢迎提交 Pull Request！

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 创建 Pull Request

---

## 许可证

Copyright (c) 2026 **SoDam AI Studio**. All rights reserved.

本软件仅供个人和教育使用。商业使用请联系发布者。详情请参阅 [LICENSE](./LICENSE)。

---

<div align="center">

*基于 Streamlit + 35个 AI 平台构建 -- SoDam AI Studio*

</div>
