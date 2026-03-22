# AI News Radar

> **自动收集、摘要、分类AI新闻的个人智能新闻仪表板**

**[English](./README.md) / [Korean](./README_KO.md) / [Japanese](./README_JA.md) / Chinese**

---

## 什么是AI News Radar？

AI News Radar是一个**个人仪表板**，自动从全球收集AI相关新闻，然后使用Google Gemini AI进行**摘要、分类和重要性评分**。

**简单来说：** 不用每天浏览15个以上的新闻网站，这个应用帮你完成，只展示重要的内容。

---

## 主要功能

| 功能 | 说明 |
|------|------|
| 自动收集 | 从15个预设来源自动收集新闻（TechCrunch、The Verge、MIT Tech Review等） |
| AI摘要 | 将每篇文章用韩语概括为3行 |
| 智能分类 | 自动分类为工具/研究/趋势/教程/商业 |
| 重要性评分 | 为每篇文章评1-5颗星 |
| 情感分析 | 将每篇文章标记为积极/中立/消极 |
| 每日简报 | 每天自动生成"今日AI新闻TOP 5" |
| 重复合并 | 多家媒体报道同一新闻时，合并为一条 |
| 关键词监控 | 高亮显示包含追踪关键词的新闻（如"Claude"、"GPT"） |
| 应用内阅读器 | 在仪表板内无广告阅读原文 |
| 暗色模式 | 暗色/亮色主题切换 |
| 导出 | 将简报和文章下载为Markdown或PDF |
| 图片分析 | AI分析新闻中的图表/信息图 |
| 实时更新 | 仪表板每5分钟自动刷新 |
| 时间线视图 | 按时间顺序浏览新闻（今天/昨天/本周） |
| Context Caching | 缓存系统提示词，API令牌成本最高减少90% |
| 智能路由 | 简单任务使用Flash-Lite，高质量任务使用Flash自动分配 |

---

## 屏幕预览

启动应用后，在浏览器中打开 `http://localhost:6601`：

- **简报选项卡** - 一览今日TOP 5 AI新闻
- **新闻列表选项卡** - 所有收集的文章 + 过滤器 + 排序
- **时间线选项卡** - 基于时间的新闻流
- **来源管理选项卡** - 管理新闻来源

---

## 开始使用（零基础逐步指南）

> **完全不需要编程经验。** 请按照每一步仔细操作。

### 第1步：安装Python

Python是运行这个应用所需的编程语言。

1. 访问 [python.org/downloads](https://www.python.org/downloads/)
2. 点击黄色大按钮 **"Download Python 3.xx"**
3. 运行下载的文件
4. **重要：** 一定要勾选安装界面底部的 **"Add Python to PATH"**
5. 点击 **"Install Now"**

**验证方法：** 打开命令提示符（按 `Win + R`，输入 `cmd`，按回车），输入：
```
python --version
```
如果显示 `Python 3.13.x` 之类的信息，就成功了！

### 第2步：下载本项目

**方式A：使用Git（推荐）**

如果已安装Git：
```
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**方式B：直接下载**

1. 访问 [GitHub仓库页面](https://github.com/sodam-ai/ai-news-radar)
2. 点击绿色 **"Code"** 按钮
3. 点击 **"Download ZIP"**
4. 将ZIP文件解压到任意文件夹

### 第3步：安装所需包

打开命令提示符，进入项目文件夹并运行：
```
cd 项目文件夹路径\ai-news-radar
pip install -r requirements.txt
```

> **这是做什么的？** 自动下载应用运行所需的工具（库）。大约需要1-2分钟。

### 第4步：获取Gemini API密钥（免费）

AI功能需要Google Gemini API密钥。**完全免费**。

1. 访问 [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. 用Google账号登录
3. 点击 **"Create API Key"**（创建API密钥）
4. 复制生成的密钥（格式为 `AIzaSy...`）

### 第5步：设置API密钥

1. 在项目文件夹中找到 `.env.example` 文件
2. 复制一份并重命名为 `.env`
3. 用文本编辑器（记事本即可）打开 `.env`
4. 将 `your_gemini_api_key_here` 替换为实际的API密钥：

```
GEMINI_API_KEY=AIzaSy在这里输入实际密钥
```

5. 保存文件

> **安全提示：** `.env` 文件包含您的秘密API密钥。此文件会自动从GitHub上传中排除。切勿与他人共享。

### 第6步：启动应用

```
streamlit run app.py
```

浏览器会自动打开 **http://localhost:6601**

完成！AI News Radar已经启动了！

---

## 使用方法

### 首次使用

1. 点击侧边栏的 **"收集"** 按钮 → 收集新闻
2. 点击 **"AI处理"** 按钮 → AI分析收集的文章
3. 点击 **"生成简报"** → 生成今日TOP 5摘要

### 日常使用

应用每60分钟自动收集新闻。打开仪表板：

- **简报选项卡** 快速浏览
- **新闻列表** 详细阅读
- 使用侧边栏 **过滤器** 聚焦特定分类/情感

### 功能指南

| 想做的事 | 方法 |
|---------|------|
| 添加新闻来源 | 侧边栏 > 来源管理 > 输入名称和RSS URL > 点击"添加来源" |
| 追踪关键词 | 侧边栏 > 关键词监控 > 输入关键词 > 点击"添加" |
| 阅读原文 | 点击文章标题（新标签页）或"查看详情" > "获取原文" |
| 导出为PDF | 简报选项卡或新闻选项卡 > "导出" > 选择PDF |
| 导出为Markdown | 简报选项卡或新闻选项卡 > "导出" > 选择Markdown |
| 切换暗色/亮色 | 侧边栏顶部的切换按钮 |
| 分类过滤 | 侧边栏 > 过滤器部分 > 选择分类 |
| 情感过滤 | 侧边栏 > 过滤器部分 > 选择情感 |
| 重要性过滤 | 侧边栏 > 过滤器部分 > 调整滑块 |

---

## 项目结构

```
ai-news-radar/
├── app.py                  # 主仪表板（浏览器中看到的界面）
├── config.py               # 配置（API密钥、收集间隔等）
├── requirements.txt        # 所需包列表
├── .env.example            # API密钥配置模板
├── .env                    # 实际API密钥（不会上传到GitHub）
├── LICENSE                 # MIT许可证（SoDam AI Studio）
├── .streamlit/
│   └── config.toml         # 主题和端口配置
├── crawler/                # 新闻收集
│   ├── rss_crawler.py      # 从RSS源获取文章
│   └── scheduler.py        # 自动收集调度器
├── ai/                     # AI处理
│   ├── model_router.py     # 智能路由 + Context Caching
│   ├── batch_processor.py  # 批量AI处理 + 图片分析
│   ├── deduplicator.py     # 重复新闻合并
│   └── briefing.py         # 今日简报TOP 5生成
├── reader/
│   └── article_reader.py   # 无广告原文阅读器
├── export/
│   └── exporter.py         # Markdown/PDF导出
├── data/
│   └── preset_sources.json # 15个预设新闻来源
├── utils/
│   └── helpers.py          # 工具函数
└── PRD/                    # 设计文档（4个文件）
```

---

## 故障排除

| 问题 | 解决方法 |
|------|---------|
| 找不到 `pip` 命令 | 重新安装Python，勾选"Add Python to PATH" |
| 找不到 `streamlit` 命令 | 运行：`pip install streamlit` |
| "GEMINI_API_KEY未设置"警告 | 确认已创建 `.env` 文件（不是 `.env.example`） |
| 没有文章显示 | 先点击"收集"，然后点击"AI处理" |
| 端口6601被占用 | 关闭其他Streamlit实例或在 `.streamlit/config.toml` 中更改端口 |
| PDF导出失败 | 仅在Windows环境下可用（使用Windows字体支持韩语） |
| 文章已收集但无AI分析 | 检查 `.env` 文件中的GEMINI_API_KEY是否正确 |
| 启动时出错 | 重新运行 `pip install -r requirements.txt` 检查缺失的包 |

---

## 免费API限额

AI News Radar使用Gemini免费层，可以**完全免费**运营：

| 模型 | 免费限额 | 用途 |
|------|---------|------|
| Gemini Flash-Lite | 1,000次/天 | 分类、标签、情感分析 |
| Gemini Flash | 250次/天 | 摘要、简报、图片分析 |

智能路由系统自动将简单任务分配给轻量模型，将复杂任务分配给高性能模型，最大化免费额度的利用。

---

## 路线图

| Phase | 主要功能 | 状态 |
|-------|---------|------|
| Phase 1 (MVP) | 收集 + AI摘要 + 仪表板（17项功能） | 已完成 |
| Phase 2 | 聊天 + 语音 + 机器人 + 事实核查 + 游戏化（35项功能） | 计划中 |
| Phase 3 | 智能体 + 预测 + 播客 + 插件 + 团队模式（19项功能） | 计划中 |

详细路线图请参阅 [PRD/03_PHASES.md](./PRD/03_PHASES.md)。

---

## 技术栈

| 组件 | 技术 | 选择原因 |
|------|------|---------|
| 语言 | Python 3.11+ | AI和Web爬虫的最佳生态系统 |
| 仪表板 | Streamlit 2026 | 仅用Python构建Web UI |
| AI | Google Gemini (Flash + Flash-Lite) | 免费层、智能路由、Context Caching |
| 数据 | 本地JSON文件 | 无需数据库服务器 |
| 调度 | APScheduler | 无需cron，在应用内自动收集 |
| PDF导出 | fpdf2 | 轻量PDF生成，韩语字体支持 |

---

## 许可证

MIT License - Copyright (c) 2026 **SoDam AI Studio**

详情请参阅 [LICENSE](./LICENSE) 文件。

---

*使用 Streamlit + Google Gemini AI 构建 — SoDam AI Studio*
