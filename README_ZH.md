# AI News Radar

> **自动收集、摘要、分类AI新闻的个人智能仪表板 — 74个来源、35个LLM平台**

**[English](./README.md) / [Korean](./README_KO.md) / [Japanese](./README_JA.md) / Chinese**

---

## 这是什么？

AI News Radar是一个**个人仪表板**，自动从全球收集AI新闻，AI进行**摘要、分类和重要性评分**。支持**35个LLM平台**（大部分免费）、**Web+桌面**双模式、可自动发布到**5个社交平台**。

---

## 主要功能（45+）

| 类别 | 功能 |
|------|------|
| **仪表板** | 每日简报、分领域简报（图像/视频、Vibe编程、本体论）、分类过滤、情感图表、语音简报、周报、邮件通讯 |
| **新闻流** | 74来源自动收集、AI摘要、9分类、事实核查、重复合并、搜索、收藏、分页 |
| **AI功能** | AI聊天、术语表、AI辩论、内容自动生成（5种）、智能提醒、工具对比（21个工具）、趋势图表 |
| **分享** | 社交发布（X/Telegram/Discord/Threads/Instagram）、卡片新闻图片、Markdown/PDF导出 |
| **桌面应用** | 原生窗口+系统托盘+后台通知 |

---

## 开始使用

> **完全不需要编程经验。**

### 第1步：安装Python
[python.org/downloads](https://www.python.org/downloads/) → 勾选 **"Add Python to PATH"**

### 第2步：下载项目
```
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

### 第3步：安装依赖
```
pip install -r requirements.txt
```

### 第4步：获取API密钥（免费）
[console.groq.com/keys](https://console.groq.com/keys) → 注册 → 创建密钥 → 复制

### 第5步：设置API密钥
将 `.env.example` 复制为 `.env` → 用记事本打开 → 输入 `GROQ_API_KEY=gsk_你的密钥`

### 第6步：启动应用
```
streamlit run app.py
```
浏览器自动打开 **http://localhost:6601**

### 第7步：首次使用
1. 点击 **"收集"** → 从74个来源收集新闻
2. 点击 **"AI处理"** → AI分析所有文章
3. 点击 **"生成简报"** → 创建今日TOP 5

---

## 使用指南

| 想要做什么 | 方法 |
|-----------|------|
| 看今日摘要 | 仪表板 > 简报 |
| 只看图像/视频新闻 | 仪表板 > 选择分类 |
| 向AI提问 | AI标签 > 聊天 |
| 对比AI工具 | 洞察标签 > 工具对比 |
| 发布到社交平台 | 分享标签 > 社交发布 |
| 语音收听 | 仪表板 > 语音按钮 |

---

## 故障排除

| 问题 | 解决 |
|------|------|
| 找不到 `pip` | 重装Python，勾选"Add to PATH" |
| 没有文章 | 先"收集"→再"AI处理" |
| 端口占用 | 使用 `--server.port 7429` |

---

## 路线图

| Phase | 状态 |
|-------|------|
| Phase 1~2（27项） | **已完成** |
| Tier 1~2 + S-Tier（9项） | **已完成** |
| UI/UX + 桌面应用 | **已完成** |
| 下一步: 自动翻译、ChromaDB、Ollama | 计划中 |

---

## 许可证

MIT License - Copyright (c) 2026 **SoDam AI Studio**

---

*使用 Streamlit + 35个AI平台构建 — SoDam AI Studio*
