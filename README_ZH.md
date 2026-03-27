<div align="center">

# AI News Radar

**您的AI驱动新闻智能平台 — 自动收集、分析并汇总来自74个新闻源的AI资讯，支持35个大语言模型。**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.44+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![LLMs](https://img.shields.io/badge/LLM平台-35个-blueviolet)](#35个llm平台)
[![Sources](https://img.shields.io/badge/新闻来源-74个-blue)](#74个新闻来源)
[![Commits](https://img.shields.io/badge/提交次数-37-orange)](#)
[![License](https://img.shields.io/badge/许可证-MIT-green)](./LICENSE)

**语言** &nbsp;/&nbsp; [한국어](./README_KO.md) &nbsp;/&nbsp; [日本語](./README_JA.md) &nbsp;/&nbsp; [English](./README.md)

</div>

---

## 什么是AI News Radar？

AI领域瞬息万变。新模型发布、工具更新、论文发表、公司转型——这些信息散落在数十个不同的网站上。**AI News Radar** 为您消除信息噪音。它持续从 **74个精选来源** 收集新闻，利用AI对每篇文章进行摘要、分类、评分和事实核查，然后以您的语言、按照您的计划、通过您偏好的平台，为您提供清晰、可执行的简报。

**一句话总结：** 无需访问74个网站，让AI全部读完，告诉您什么是重要的。

---

## 🔒 安全与隐私 — 请先阅读

> **在使用本项目之前，请务必先阅读本章节。这是最重要的部分。**

### 关于API密钥，您需要了解的一切

本项目 **不包含任何API密钥**。以下是关于安全性的重要说明：

| 问题 | 答案 |
|------|------|
| 项目中内置了API密钥吗？ | **没有。** 本项目完全不包含任何API密钥 |
| 我的API密钥会被上传到GitHub吗？ | **绝对不会。** `.env`文件已被加入`.gitignore`，永远不会被上传 |
| 别人能看到我的API密钥吗？ | **不能。** 您的密钥只保存在您自己的电脑上，不会离开您的设备 |
| 我需要花钱购买API密钥吗？ | **不需要。** 有多个完全免费的高额度选项可供选择 |
| 每个用户需要各自的密钥吗？ | **是的。** 每位用户必须自己申请并使用自己的私人密钥 |

### 工作原理示意图

```
您的电脑（本地）                      互联网 / GitHub
┌──────────────────────────┐          ┌─────────────────────┐
│  .env 文件（仅在本机）    │          │  GitHub 公开仓库     │
│                          │    ✗     │                     │
│  GROQ_API_KEY=gsk_xxxxx  │──────────│  只有程序代码文件    │
│  （您的私人密钥）         │  永不上传 │  没有任何API密钥     │
│                          │          │                     │
└──────────────────────────┘          └─────────────────────┘
         ↓ 只在本机使用
   AI服务（Groq / Gemini等）
```

### 推荐的免费API密钥（两个最佳选项）

| 平台 | 免费额度 | 申请地址 | 特点 |
|------|---------|---------|------|
| **Google Gemini** ⭐ | 每天 **1,000次** 免费调用 | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | 用Gmail账号即可登录 |
| **Groq** ⭐ | 每天 **14,400次** 免费调用 | [console.groq.com/keys](https://console.groq.com/keys) | 注册极为简单，速度最快 |

> **建议：** 对于初次使用，强烈推荐选择 **Groq**（10秒完成注册，额度最充足）或 **Google Gemini**（使用已有的Google账号即可）。

---

## 无需API密钥的功能 vs 需要API密钥的功能

| 功能 | 无需API密钥 | 需要API密钥 |
|------|:-----------:|:-----------:|
| 收集新闻（RSS抓取） | ✅ | |
| 浏览新闻列表 | ✅ | |
| 书签与分页浏览 | ✅ | |
| 关键词搜索 | ✅ | |
| 时间线视图 | ✅ | |
| 应用内文章阅读器 | ✅ | |
| AI摘要生成 | | ✅ |
| 9类别自动分类 | | ✅ |
| 重要度评分（1-5星） | | ✅ |
| 情感分析 | | ✅ |
| AI事实核查 | | ✅ |
| 每日简报生成 | | ✅ |
| AI新闻聊天 | | ✅ |
| AI词汇表 | | ✅ |
| AI辩论 | | ✅ |
| 每周智能报告 | | ✅ |
| SNS内容自动生成 | | ✅ |
| 语音简报（TTS） | | ✅ |

---

## 主要特性

- **50+个功能** 分布在5个标签页（仪表盘 / 新闻流 / AI / 洞察 / 分享）
- **74个来源** — 通用AI (26) + 图像与视频 (20) + AI编程 (19) + 本体论 (9)
- **35个LLM平台** — 大多数提供免费套餐，只需任意一个API密钥
- **9个分类** — 工具、研究、趋势、教程、商业、图像/视频、AI编程、本体论、其他
- **19个追踪的AI工具** 支持自动版本发布检测
- **5个SNS平台** — X、Telegram、Discord、Threads、Instagram + 自动生成卡片新闻
- **5种内容类型** — 推文、帖子串、Instagram说明、博客文章、LinkedIn帖子
- **语音简报**、AI事实核查、AI词汇表、AI辩论
- **一键完整流程** — 收集 > 分析 > 简报 > 版本检测
- **桌面应用** 支持系统托盘与后台通知
- **GitHub Actions** — 每日自动收集3次
- **自动韩语翻译**（英语转韩语）

---

## 功能列表（50+）

### 仪表盘标签页

| 功能 | 说明 |
|------|------|
| 每日简报 | AI生成"今日AI新闻Top 5"，按重要度排序 |
| 专题简报 | 图像/视频、AI编程、本体论的专项独立简报 |
| 分类快速筛选 | 一键筛选9个分类中的任意一个 |
| 情感仪表盘 | 交互式Plotly图表，展示正面/中性/负面比例 |
| 语音简报 | 通过edge-tts将简报转为AI语音朗读 |
| 每周智能报告 | 自动生成包含趋势、预测和分析的每周报告 |
| 新闻通讯 | 通过电子邮件（SMTP）发送每日或每周简报 |

### 新闻流标签页

| 功能 | 说明 |
|------|------|
| 74源采集 | 使用15个并发Worker进行高速并行抓取 |
| AI摘要 | 为每篇文章生成3行韩语摘要 |
| 9类别分类 | AI自动分类 |
| 重要度评分 | 每篇文章1–5星评级 |
| 情感分析 | 正面/中性/负面标签 |
| AI事实核查 | 跨来源交叉核验（"3家媒体确认"vs"单一来源"）|
| 重复合并 | 多家媒体报道的同一故事自动合并 |
| 关键词监控列表 | 高亮显示并提醒您关注的关键词 |
| 应用内阅读器 | 在仪表盘内全文阅读（无广告）|
| 高级搜索 | 按关键词、分类、情感、阅读状态筛选 |
| 书签与备注 | 保存文章并附加个人笔记 |
| 分页浏览 | 每页10篇文章，流畅翻页 |
| 时间线视图 | 按今天/昨天/本周浏览 |
| 自动韩语翻译 | 英语文章自动翻译成韩语 |

### AI标签页

| 功能 | 说明 |
|------|------|
| AI新闻聊天 | 用自然语言提问已收集的新闻内容 |
| AI词汇表 | 自动提取AI术语，附带初学者友好的解释 |

### 洞察标签页

| 功能 | 说明 |
|------|------|
| AI工具版本追踪器 | 追踪19个AI工具，自动检测版本发布 |
| 趋势图表 | 每日提及频次的交互式Plotly折线图 |
| 热门关键词 | 上升趋势关键词及周环比变化率 |
| AI辩论 | "Midjourney vs Flux" — AI生成正反论点与最终裁定 |
| 每周智能报告 | 含预测的深度每周分析 |

### 分享标签页

| 功能 | 说明 |
|------|------|
| SNS自动发布 | 发布到X、Telegram、Discord、Threads和Instagram |
| 卡片新闻生成器 | 自动生成1080×1080卡片图（深色主题，按分类配色）|
| AI内容生成 | 自动生成推文、帖子串、Instagram说明、博客文章、LinkedIn帖子 |
| 新闻通讯邮件 | 向订阅者列表发送格式化简报 |
| 导出 | 下载为Markdown或PDF格式 |

### 系统功能

| 功能 | 说明 |
|------|------|
| 一键完整流程 | 一键完成采集 > AI处理 > 简报生成 > 版本检测 |
| 并行抓取 | 15个并发Worker，高速采集 |
| 批量并行处理 | 大批量文章的高效AI批处理 |
| 智能关键词提醒 | 监控关键词出现时推送桌面通知 |
| 桌面应用 | 基于pywebview的原生窗口 + 系统托盘 + 后台模式 |
| GitHub Actions | 每日自动采集3次（可配置）|
| Telegram机器人 | 7条指令，随时随地访问 |

---

## 74个新闻来源

| 分类 | 数量 | 示例 |
|------|:----:|------|
| **通用AI** | 26 | TechCrunch、The Verge、MIT Tech Review、Wired、ZDNET、Ben's Bites、Ars Technica |
| **图像与视频** | 20 | Stability AI、Civitai、Runway、Reddit（StableDiffusion、midjourney、flux_ai、comfyui）|
| **AI编程** | 19 | Cursor、GitHub、Anthropic、Simon Willison、Reddit（vibecoding、ClaudeAI、cursor）|
| **本体论** | 9 | Neo4j、Stardog、W3C、Reddit（semanticweb、KnowledgeGraphs）|

---

## 35个LLM平台

您只需要从以下平台中选择 **任意一个** API密钥：

| 等级 | 平台 |
|------|------|
| **免费（推荐）** | Gemini、Groq、Cerebras、SambaNova、xAI、Mistral、Cohere、HuggingFace、NVIDIA、Cloudflare、智谱AI、Kluster、GLHF、Hyperbolic |
| **积分 / 低价** | Together AI、OpenRouter、Fireworks、DeepSeek、DeepInfra、Perplexity、AI21、Upstage、Lepton、Novita、Nebius、Chutes、Replicate、阿里云、Moonshot、Yi、百川 |
| **付费** | OpenAI、Azure OpenAI、Anthropic Claude、Reka AI |

> **提示：** Gemini和Groq是最容易配置且免费额度最充足的选项，强烈推荐初次使用者选择。

---

## 仪表盘概览（5个标签页）

| 标签页 | 内容 |
|--------|------|
| **仪表盘** | 每日简报、专题简报、分类快速筛选、情感图表、每周报告、新闻通讯 |
| **新闻流** | 全部新闻、高级搜索、书签、时间线视图、分页浏览 |
| **AI** | 新闻聊天、AI词汇表 |
| **洞察** | 版本追踪器、趋势图表、热门关键词、AI辩论、每周报告 |
| **分享** | SNS发布、AI内容生成、卡片新闻、新闻通讯、导出 |

---

## 快速开始 — 完全新手指南

> **零编程经验也可以使用。** 即使您从未打开过终端，也请放心，下面的每个步骤都有非常详细的说明。

### 什么是"终端"？在开始之前先了解这个

**终端**（也叫"命令提示符"或"控制台"）是您通过输入文字命令来控制电脑的工具。本指南中需要用到它。

**如何在Windows上打开终端：**
1. 同时按下键盘上的 `Win键（Windows徽标键）` 和 `R键`
2. 屏幕上会弹出一个小窗口，在里面输入 `cmd`
3. 按下 `Enter键`（回车键）
4. 一个黑色背景的窗口就出现了——这就是终端，不用害怕它

**如何在终端中输入命令：**
- 把命令复制粘贴到终端窗口中
- 按 `Enter键` 执行命令
- 等待命令完成（有时需要等一会儿）

---

### 第1步 — 安装Python

Python是运行本程序所需的编程语言环境。免费下载，全球数百万人使用。

1. 打开浏览器，访问 [python.org/downloads](https://www.python.org/downloads/)
2. 点击页面上醒目的 **"Download Python"**（下载Python）大按钮
3. 文件下载完成后，双击运行该安装文件
4. ⚠️ **极其重要，绝对不能忘记：** 在安装界面的**最底部**，找到并勾选 **"Add Python to PATH"** 这个复选框
   - 如果忘记勾选这一步，Python将无法被终端识别，后面的步骤将全部失败
   - 务必先勾选，再点击安装
5. 点击 **"Install Now"**（立即安装）
6. 等待安装完成，看到"Setup was successful"表示成功

**验证Python是否安装成功：**

打开终端，输入以下命令并按回车：

```bash
python --version
```

如果看到类似 `Python 3.11.x` 或更高版本的文字，说明安装成功！

> **遇到问题？** 如果提示"'python'不是内部或外部命令"，请关闭终端，重新安装Python，并**确保勾选了"Add Python to PATH"**，然后再打开新终端重试。

---

### 第2步 — 下载项目

**方法A：使用Git下载（推荐，如果您已安装Git）**

在终端中输入以下两行命令（每行按一次回车）：

```bash
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**方法B：直接下载ZIP压缩包（更简单，推荐新手使用）**

1. 用浏览器打开 [GitHub仓库页面](https://github.com/sodam-ai/ai-news-radar)
2. 找到并点击绿色的 **"Code"** 按钮
3. 在弹出菜单中点击 **"Download ZIP"**（下载ZIP）
4. 下载完成后，找到下载的ZIP文件
5. 右键点击ZIP文件，选择"全部解压缩..."或"解压到当前文件夹"
6. 记住解压后文件夹的位置（例如：`C:\Users\您的用户名\Downloads\ai-news-radar`）

**在解压后的项目文件夹中打开终端（Windows专用方法）：**
1. 打开"文件资源管理器"（就是平时浏览文件的窗口）
2. 进入刚才解压的 `ai-news-radar` 文件夹
3. 点击顶部地址栏（显示文件夹路径的长条），路径文字会变蓝选中
4. 直接输入 `cmd`（会覆盖原来的路径）
5. 按回车键
6. 终端就会在这个文件夹中打开了

---

### 第3步 — 创建虚拟环境（推荐）

虚拟环境是为这个项目单独创建的Python工作空间，可以防止与您电脑上其他Python项目发生冲突。

在终端中输入以下命令并按回车：

```bash
python -m venv venv
```

等待命令完成（大约10-30秒），然后**激活**虚拟环境：

```bash
# Windows系统（使用这条命令）
venv\Scripts\activate

# macOS / Linux系统（使用这条命令）
source venv/bin/activate
```

激活成功的标志：您会看到终端提示符行首多了 `(venv)` 字样，例如：
```
(venv) C:\Users\您的名字\ai-news-radar>
```

> **重要提示：** 每次重新打开终端来使用本项目时，都需要先重新执行激活命令。

---

### 第4步 — 安装依赖包

依赖包是程序正常运行所需要的各种工具库。在终端中输入以下命令：

```bash
pip install -r requirements.txt
```

这条命令会自动下载并安装所有必要的包。**请耐心等待，可能需要1-3分钟。**

在安装过程中您会看到大量滚动的文字，这是完全正常的。等到出现类似"Successfully installed..."的提示，并且光标可以继续输入时，说明安装完成。

> **网络速度慢？** 如果下载很慢，可以使用国内镜像加速：
> ```bash
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

---

### 第5步 — 获取免费API密钥

API密钥是您访问AI服务的"通行证"。以下是两个最推荐的完全免费选项：

#### 推荐选项A：Groq（每天14,400次免费，注册极简单）

1. 打开浏览器，访问 [console.groq.com/keys](https://console.groq.com/keys)
2. 点击"Sign in with Google"，用您的 **Google账号** 登录（整个过程约10秒）
3. 登录后点击 **"Create API Key"**（创建API密钥）按钮
4. 在"Name"栏随便起个名字（例如：`my-news-radar`），点击确认
5. 屏幕上会显示您的API密钥，以 `gsk_` 开头，例如：`gsk_abc123xyz...`
6. **立即复制并保存这个密钥**（它只显示一次！关闭窗口后无法再查看）

#### 推荐选项B：Google Gemini（每天1,000次免费，使用Gmail账号）

1. 打开浏览器，访问 [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. 使用您的 **Gmail账号** 登录
3. 点击 **"创建API密钥"** 按钮
4. 复制生成的密钥（一长串字母和数字）
5. 将密钥保存在安全的地方

> **其他免费选项：** [Cerebras](https://cloud.cerebras.ai/)、[SambaNova](https://cloud.sambanova.ai/)

---

### 第6步 — 配置API密钥

现在需要把您的API密钥告诉程序。请按以下步骤操作：

1. 在项目文件夹中找到名为 **`.env.example`** 的文件
   - 提示：Windows默认不显示以"."开头的文件，如果看不到，请在文件资源管理器中点击"查看" > 勾选"隐藏的项目"
2. **复制**这个文件（右键 > 复制），然后在同一文件夹中**粘贴**（右键 > 粘贴）
3. 将复制出来的文件重命名为 **`.env`**（删掉`.example`这部分）
4. 用**记事本**打开 `.env` 文件（右键 > 打开方式 > 记事本）
5. 找到对应的行，填入您的API密钥：

```env
# 如果使用Groq，把下面这行的引号内容替换为您的实际密钥：
GROQ_API_KEY=gsk_您的实际密钥粘贴在这里

# 如果使用Gemini，把下面这行的#号删掉，并填入您的密钥：
# GEMINI_API_KEY=您的gemini密钥粘贴在这里

# 如果使用OpenAI：
# OPENAI_API_KEY=sk-您的openai密钥
```

6. 保存文件（按 `Ctrl+S`）并关闭记事本

> **安全提醒：**
> - `.env` 文件已被加入 `.gitignore`，**永远不会被上传到GitHub**
> - 这个文件只存在于您自己的电脑上
> - 请不要把这个文件分享给任何人，也不要截图发给别人

---

### 第7步 — 启动程序

一切就绪！现在可以启动程序了。

**网页模式（推荐，在浏览器中打开）：**

```bash
streamlit run app.py
```

程序启动后，浏览器会自动打开并跳转到 **http://localhost:6601**

如果浏览器没有自动打开，请手动在浏览器地址栏输入：`http://localhost:6601`

**桌面模式（原生独立窗口）：**

```bash
python desktop.py
```

**Windows一键启动（最简单）：**

直接双击项目文件夹中的 **`AI_News_Radar.bat`** 文件即可启动，无需打开终端。

---

### 首次使用流程

程序成功打开后，请按照以下顺序操作，即可获得第一份AI新闻简报：

1. 点击左侧边栏的 **"Collect"（收集）** 按钮
   - 程序会开始从74个来源抓取最新新闻，约需1分钟，请耐心等待
2. 收集完成后，点击 **"AI Process"（AI处理）** 按钮
   - AI将对所有文章进行分析、摘要和自动分类
3. 点击 **"Generate Briefing"（生成简报）** 按钮
   - 生成今日AI新闻Top 5简报
4. 开始探索5个标签页，发现所有功能！

---

## 使用指南

| 您想做什么 | 如何操作 |
|-----------|---------|
| 阅读今日摘要 | 仪表盘标签页 > 简报区域 |
| 按分类筛选 | 仪表盘标签页 > 点击分类快速筛选按钮 |
| 搜索某个话题 | 新闻流标签页 > 搜索视图 > 输入关键词 |
| 向AI提问新闻内容 | AI标签页 > 聊天视图 > 输入您的问题 |
| 查询AI术语含义 | AI标签页 > 词汇表视图 > 浏览或搜索 |
| 追踪AI工具版本发布 | 洞察标签页 > 版本追踪器 |
| 查看热门关键词趋势 | 洞察标签页 > 趋势 |
| 发起AI辩论 | 洞察标签页 > AI辩论 > 选择两个工具 |
| 生成SNS发布内容 | 分享标签页 > 内容生成 > 选择文章 + 平台 |
| 发布到社交媒体 | 分享标签页 > SNS发布 > 选择平台 > 发布 |
| 收听语音简报 | 仪表盘标签页 > 选择声音 > 点击"语音"按钮 |
| 导出为PDF | 分享标签页 > 导出视图 |
| 保存收藏文章 | 新闻流标签页 > 点击任意文章的书签图标 |
| 设置关键词提醒 | 左侧边栏 > 监控列表 > 输入关键词 |
| 一键运行完整流程 | 左侧边栏 > "一键完整流程"按钮 |

---

## SNS平台配置

| 平台 | 配置时间 | 难度 | 说明 |
|------|:--------:|:----:|------|
| Discord | 30秒 | 非常简单 | 在频道设置中创建Webhook URL |
| Telegram | 2分钟 | 简单 | 通过@BotFather创建机器人 |
| X（Twitter） | 10分钟 | 中等 | 申请开发者账号 |
| Threads | 10分钟 | 中等 | Meta开发者门户 |
| Instagram | 15分钟 | 复杂 | Instagram Graph API配置 |

详细的分步骤配置说明请查看应用内的 **分享标签页 > SNS发布** 部分。

---

## 项目结构

```
ai-news-radar/
├── app.py                       # 主仪表盘（5个标签页）
├── desktop.py                   # 桌面应用（pywebview + 系统托盘）
├── config.py                    # 设置（9个分类、端口、路径）
├── requirements.txt             # 依赖包列表
├── .env.example                 # API密钥模板
├── AI_News_Radar.bat            # Windows启动器（网页模式）
├── AI_News_Radar_Silent.vbs     # 静默启动器（无控制台窗口）
│
├── ai/                          # 14个AI模块
│   ├── model_router.py          #   35个LLM提供商路由
│   ├── briefing.py              #   每日+专题简报生成
│   ├── chat.py                  #   自然语言新闻聊天
│   ├── voice_briefing.py        #   TTS语音输出（edge-tts）
│   ├── factcheck.py             #   跨来源事实核查
│   ├── glossary.py              #   AI术语词典
│   ├── weekly_report.py         #   每周智能报告
│   ├── competitor.py            #   AI工具版本监控
│   ├── release_tracker.py       #   自动版本发布检测
│   ├── trend.py                 #   关键词趋势分析
│   ├── debate.py                #   AI辩论模式
│   ├── smart_alert.py           #   桌面关键词通知
│   ├── translator.py            #   自动韩语翻译
│   ├── deduplicator.py          #   重复文章合并
│   └── batch_processor.py       #   批量并行处理
│
├── sns/                         # SNS与分享模块
│   ├── card_generator.py        #   1080×1080卡片新闻图片（Pillow）
│   ├── poster.py                #   5平台SNS发布
│   ├── content_generator.py     #   AI内容生成（5种类型）
│   └── newsletter.py            #   电子邮件新闻通讯（SMTP）
│
├── crawler/                     # 数据采集
│   ├── rss_crawler.py           #   RSS源爬虫（15个并行Worker）
│   └── scheduler.py             #   基于APScheduler的定时任务
│
├── bot/                         # Telegram集成
│   └── telegram_bot.py          #   Telegram机器人（7条指令）
│
├── reader/                      # 文章阅读
│   └── article_reader.py        #   无广告应用内文章阅读器
│
├── export/                      # 数据导出
│   └── exporter.py              #   Markdown + PDF导出
│
├── utils/                       # 共享工具
│   └── helpers.py               #   通用辅助函数
│
├── scripts/                     # 命令行工具
│   ├── collect.py               #   独立采集脚本
│   └── reclassify.py            #   分类重新归类工具
│
├── data/                        # 本地数据存储
│   ├── preset_sources.json      #   74个精选来源定义
│   ├── sources.json             #   活跃来源配置
│   ├── articles.json            #   已采集文章
│   ├── briefings.json           #   已生成简报
│   ├── weekly_reports.json      #   每周报告存档
│   ├── release_log.json         #   工具版本发布历史
│   ├── audio/                   #   语音简报音频文件
│   └── cards/                   #   生成的卡片新闻图片
│
├── .github/workflows/
│   └── collect.yml              #   GitHub Actions（每日自动采集3次）
│
└── PRD/                         #   产品设计文档
```

**8个目录下共24个模块** — **37次提交**，持续更新中。

---

## 技术栈

| 组件 | 技术 |
|------|------|
| **编程语言** | Python 3.11+ |
| **仪表盘** | Streamlit 1.44+ |
| **AI引擎** | 通过统一模型路由器支持35个LLM平台 |
| **图表** | Plotly（交互式趋势图表、情感仪表盘）|
| **语音** | edge-tts（微软神经TTS）|
| **图片生成** | Pillow（深色主题卡片新闻）|
| **桌面** | pywebview + pystray（原生窗口 + 系统托盘）|
| **通知** | plyer（跨平台桌面提醒）|
| **RSS解析** | feedparser（74个源的RSS订阅）|
| **网络爬虫** | BeautifulSoup4 + requests |
| **Telegram机器人** | python-telegram-bot |
| **SNS API** | tweepy（X）、Telegram API、Discord Webhook、Threads API、Instagram Graph API |
| **电子邮件** | smtplib（SMTP新闻通讯）|
| **PDF导出** | fpdf2（支持韩文/中文字体）|
| **定时任务** | APScheduler（应用内）、GitHub Actions（CI/CD）|
| **数据存储** | 本地JSON（无需数据库配置）|

---

## 常见问题解决

| 问题 | 解决方法 |
|------|---------|
| 提示找不到 `python` 命令 | 重新安装Python，安装时务必勾选 **"Add to PATH"** |
| 提示找不到 `pip` 命令 | 改用 `python -m pip install -r requirements.txt` |
| 提示找不到 `streamlit` | 运行 `pip install streamlit`，检查虚拟环境是否已激活 |
| 显示"API密钥未设置"警告 | 创建 `.env` 文件并填入至少一个API密钥（参考第6步）|
| 没有文章显示 | 先点击 **"Collect"（收集）**，再点击 **"AI Process"（AI处理）**|
| 分类显示0篇文章 | 运行 `python scripts/reclassify.py` 重新分类已有文章 |
| 端口6601已被占用 | 使用 `streamlit run app.py --server.port 7777` |
| macOS/Linux上PDF导出失败 | PDF导出使用Windows韩文字体，请安装 `NanumGothic` 字体 |
| 桌面模式无法启动 | 确认已安装pywebview：`pip install pywebview` |
| 采集速度缓慢 | 正常现象 — 74个来源使用15个并行Worker约需60秒 |
| Edge-tts语音出错 | 检查网络连接，edge-tts需要访问互联网才能工作 |
| pip安装速度很慢 | 使用国内镜像：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple` |

---

## 路线图

| 阶段 | 功能 | 状态 |
|------|------|:----:|
| **Phase 1** | 采集 + AI摘要 + 仪表盘（17个功能）| ✅ 已完成 |
| **Phase 2-A** | 搜索 + 书签 + 情感分析 + 聊天（5个功能）| ✅ 已完成 |
| **Phase 2-B** | 语音 + Telegram + 事实核查 + 词汇表 + Actions（5个功能）| ✅ 已完成 |
| **Tier 1** | 专题简报 + 每周报告 + 版本追踪器（3个功能）| ✅ 已完成 |
| **Tier 2** | 趋势图表 + AI辩论 + 热门关键词（3个功能）| ✅ 已完成 |
| **S级功能** | 智能提醒 + 内容生成 + 新闻通讯 + SNS（4个功能）| ✅ 已完成 |
| **UI/UX** | 5标签页重设计 + 分页 + 分类快速筛选 + 精美CSS | ✅ 已完成 |
| **桌面应用** | pywebview + 系统托盘 + 后台通知 | ✅ 已完成 |
| **流程优化** | 一键完整流程 + 并行抓取 + 批量处理 | ✅ 已完成 |
| **翻译** | 自动韩语翻译 + 去重 | ✅ 已完成 |
| **下一步** | ChromaDB向量搜索、Ollama本地LLM、游戏化、移动端PWA | 📋 计划中 |

---

## 参与贡献

欢迎贡献代码！请随时提交Pull Request。

1. Fork本仓库
2. 创建您的功能分支（`git checkout -b feature/amazing-feature`）
3. 提交您的更改（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 打开一个Pull Request

---

## 许可证

MIT License — Copyright (c) 2026 **SoDam AI Studio**

详情请参阅 [LICENSE](./LICENSE) 文件。

---

<div align="center">

*Streamlit + 35 AI平台 by SoDam AI Studio*

</div>
