# AI News Radar

<p align="center">
  <img src="assets/icon.png" width="80" alt="AI News Radar Icon" />
</p>
<p align="center">
  <strong>个人AI新闻情报平台</strong><br/>
  从74个来源自动收集、摘要和分析AI新闻
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-SoDam%20AI%20Studio-green"/>
  <img src="https://img.shields.io/badge/Release-v1.2.0-blue"/>
  <img src="https://img.shields.io/badge/LLM-35%20Providers-purple"/>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README_KO.md">한국어</a> |
  <a href="README_JA.md">日本語</a> |
  <a href="README_ZH.md">中文</a>
</p>

---

## 快速开始（4步）

> **不需要编程经验。**

### 第1步：安装Python
1. 访问 **[python.org/downloads](https://www.python.org/downloads/)**
2. 点击 **"Download Python"**
3. 运行安装程序
4. **重要：勾选 "Add Python to PATH"！**
5. 点击 **"Install Now"**

### 第2步：下载
从[Releases页面](https://github.com/sodam-ai/ai-news-radar/releases)下载 **`AI_News_Radar_v1.2.0.zip`** → 解压

### 第3步：获取免费API密钥
1. 访问 **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. 用Google账号登录 → **"Create API Key"** → 复制密钥

> **真的免费？** 是的！Google每天提供1,000次免费API调用。个人使用完全足够。

### 第4步：运行
**双击 `AI_News_Radar.exe`**

**首次运行时：**
- 自动创建虚拟环境并安装所有依赖
- **需要3-5分钟**（下载约200MB）
- 文本编辑器打开后，粘贴API密钥并保存
- 浏览器会自动打开AI News Radar！

**之后运行：** 双击exe → 几秒内启动

---

## 主要功能（45+）

### 新闻收集
- **74个RSS来源**自动收集（英语+韩语）
- 重复新闻自动合并、关键词监控、自动翻译

### AI分析
- 每日TOP 5简报、周度报告、AI聊天
- 趋势分析、发布追踪、竞品比较、辩论模式、术语词典、事实核查

### 内容与分享
- 语音简报（TTS）、Markdown/PDF导出
- Discord、Telegram、X、Threads、Instagram发布
- AI内容自动生成、邮件通讯

### 支持35个AI服务商
Google Gemini（推荐·免费）、Groq、OpenAI、Anthropic、Mistral、Cohere 等

---

## 环境变量

| 变量 | 必需 | 说明 |
|------|------|------|
| `GEMINI_API_KEY` | 推荐 | Google Gemini（免费：1,000次/天） |
| `GROQ_API_KEY` | 替代 | Groq（免费：14,400次/天） |
| `OPENAI_API_KEY` | 替代 | OpenAI GPT（付费） |

35个服务的完整列表见 `.env.example`。

---

## 常见问题

**显示 "API key not configured"** → 检查 `.env` 文件中的API密钥

**双击exe没有反应** → 确认Python安装时勾选了 "Add to PATH"

**首次启动很慢** → 正常！正在下载约200MB的包（3-5分钟）

**Mac/Linux** → 在终端运行：
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 6601
```

---

## 许可证

Copyright (c) 2026 **SoDam AI Studio**. All rights reserved.

本软件仅供个人和教育使用。
