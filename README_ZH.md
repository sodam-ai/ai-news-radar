# AI News Radar

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-SoDam%20AI%20Studio-green)
![Release](https://img.shields.io/badge/Release-v1.1.0-blue)

[English](README.md) | [한국어](README_KO.md) | [日本語](README_JA.md) | [中文](README_ZH.md)

---

**AI News Radar** 从 **74个新闻来源** 自动收集AI相关新闻，并通过AI进行摘要、分类和分析的个人新闻平台。

---

## 运行方法（3步）

> **完全不需要编程经验。** 只需按照以下3步操作即可。

### 第1步：下载

点击本页面顶部的绿色 **"Code"** 按钮，然后点击 **"Download ZIP"**。

将下载的ZIP文件解压到任意文件夹。

### 第2步：安装Python

如果已经安装了Python，请跳过此步骤。

1. 访问 **[python.org/downloads](https://www.python.org/downloads/)**
2. 点击黄色的 **"Download Python"** 按钮
3. 运行下载的文件
4. **重要：勾选底部的 "Add Python to PATH" 复选框！**
5. 点击 **"Install Now"**

### 第3步：运行应用

打开解压后的文件夹，**双击**以下文件：

| 文件 | 说明 |
|------|------|
| **`install_and_run.bat`** | **首次运行时使用。** 自动安装所有依赖并引导设置API密钥。 |
| **`start.bat`** | **之后运行时使用。** 快速启动。 |

完成！浏览器将打开AI News Radar。

---

## 获取免费API密钥

AI News Radar需要AI服务来分析新闻。推荐使用免费的 **Google Gemini**。

1. 访问 **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. 使用Google账号登录
3. 点击 **"Create API Key"**
4. 复制密钥

运行 `install_and_run.bat` 时会自动引导您输入密钥。

> **支持35个AI服务。** 查看 `.env.example` 获取完整列表。只需要1个密钥即可。

---

## 主要功能（45+）

### 新闻收集
- 从 **74个RSS来源** 自动收集（英语+韩语）
- 重复新闻自动合并
- 关键词监控列表
- 英文文章自动翻译为韩语

### AI分析
- **一键流水线**：收集→分析→简报一键完成
- 每日TOP 5简报自动生成
- 周度情报报告
- AI聊天（关于新闻提问）
- 趋势分析+图表
- AI工具发布追踪
- 竞品比较
- AI辩论模式（正反分析）
- AI术语词典
- 事实核查
- 智能提醒

### 内容与分享
- 语音简报（TTS）
- Markdown / PDF导出
- 发布到Discord、Telegram、X、Threads、Instagram
- AI内容自动生成
- 邮件通讯发布

---

## 环境变量

所有设置存储在 `.env` 文件中。至少需要1个API密钥。

| 变量 | 必需 | 说明 |
|------|------|------|
| `GEMINI_API_KEY` | 推荐 | Google Gemini（免费：1000次/天） |
| `GROQ_API_KEY` | 替代 | Groq（免费：14,400次/天） |
| `OPENAI_API_KEY` | 替代 | OpenAI GPT（付费） |

---

## 常见问题

**Q：显示 "API key not configured"**
A：用记事本打开 `.env` 文件，确认API密钥已正确输入。

**Q：双击.bat文件没有反应**
A：右键点击.bat文件→选择"以管理员身份运行"。

**Q：可以在Mac或Linux上使用吗？**
A：可以！在终端运行以下命令：
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 6601
```

---

## 许可证

Copyright (c) 2026 **SoDam AI Studio**. All rights reserved.

本软件仅供个人和教育使用。商业使用请联系发布者。
