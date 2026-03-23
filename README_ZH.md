# AI News Radar

> **自动收集、摘要、分类AI新闻的个人智能新闻仪表板 — 支持35个LLM平台**

**[English](./README.md) / [Korean](./README_KO.md) / [Japanese](./README_JA.md) / Chinese**

---

## 什么是AI News Radar？

AI News Radar是一个**个人仪表板**，自动从全球收集AI相关新闻，然后使用AI进行**摘要、分类和重要性评分**。支持OpenAI、Gemini、Groq、Claude等**35个LLM平台**，大部分可免费使用。

**简单来说：** 不用每天浏览15个以上的新闻网站，这个应用帮你完成，只展示重要的内容。

---

## 主要功能（27项）

### Phase 1 — 核心（17项）

| 功能 | 说明 |
|------|------|
| 自动收集 | 从15个预设来源自动收集新闻 |
| AI摘要 | 将每篇文章用韩语概括为3行 |
| 智能分类 | 自动分为6个类别：工具、研究、趋势、教程、商业、其他 |
| 重要性评分 | 为每篇文章评1-5颗星 |
| 情感分析 | 将每篇文章标记为积极/中立/消极 |
| 每日简报 | 每天自动生成"今日AI新闻TOP 5" |
| 重复合并 | 多家媒体报道同一新闻时合并为一条 |
| 关键词监控 | 高亮显示包含追踪关键词的新闻 |
| 应用内阅读器 | 在仪表板内无广告阅读原文 |
| 暗色模式 | 暗色/亮色主题切换 |
| 导出（Markdown/PDF） | 下载简报和文章 |
| 图片分析 | AI分析新闻中的图表/信息图 |
| 实时更新 | 每5分钟自动刷新 |
| 时间线视图 | 按时间顺序浏览新闻 |
| Context Caching | 减少API令牌成本 |
| 智能路由 | 根据任务自动选择模型 |

### Phase 2-A — 扩展（5项）

| 功能 | 说明 |
|------|------|
| 搜索 | 关键词+分类+情感+已读状态搜索 |
| 书签+备注 | 保存重要文章并添加备注 |
| 已读历史 | 已读标记+未读过滤 |
| 情感温度计 | Plotly图表：仪表盘+环形图+堆叠柱状图 |
| AI聊天 | 用自然语言向收集的新闻提问 |

### Phase 2-B — 高级（5项）

| 功能 | 说明 |
|------|------|
| 语音简报 | 用AI语音收听每日简报（edge-tts，男/女声选择） |
| AI事实核查 | 交叉验证徽章："✅ N家媒体确认" vs "⚠️ 单一来源" |
| AI术语表 | 自动提取新闻中的AI专业术语 + 初学者友好解释（难度/类别过滤） |
| Telegram机器人 | `/today` 简报、`/top` 新闻、`/search` 搜索、`/ask` AI聊天 |
| GitHub Actions | 每日3次自动收集（06/12/18时 KST），手动触发，CLI脚本 |

---

## 支持35个LLM平台

以下平台中**任选一个**的API密钥即可：

### 充足的免费额度（推荐）

| 平台 | 免费额度 | 获取密钥 |
|------|---------|---------|
| Google Gemini | Flash-Lite 1,000/天、Flash 250/天 | [aistudio.google.com](https://aistudio.google.com/apikey) |
| Groq | 30/分、14,400/天 | [console.groq.com](https://console.groq.com/keys) |
| Cerebras | 30/分（超快速） | [cloud.cerebras.ai](https://cloud.cerebras.ai/) |
| xAI (Grok) | 每月$25积分 | [console.x.ai](https://console.x.ai/) |
| NVIDIA NIM | 1,000积分 | [build.nvidia.com](https://build.nvidia.com/) |
| + 9个以上 | 参见 .env.example | 各网站 |

### 注册积分/低价（17个） · 付费（4个）

详情请参阅 `.env.example` 文件。

---

## 仪表板（8个选项卡）

| 选项卡 | 功能 |
|--------|------|
| **📋 简报** | 今日TOP 5 + 情感温度计 + 语音简报（MP3） |
| **📰 新闻** | 全部文章 + 过滤器 + 书签/已读 + 事实核查徽章 |
| **🔍 搜索** | 关键词 + 分类 + 情感 + 已读状态过滤 |
| **💬 AI聊天** | 用自然语言询问新闻 |
| **📚 术语表** | AI专业术语初学者解释（难度/类别过滤） |
| **⏰ 时间线** | 时间顺序新闻流 |
| **⭐ 书签** | 已保存文章 + 备注编辑 |
| **📡 来源** | 15个新闻来源管理 |

---

## 开始使用（零基础逐步指南）

> **完全不需要编程经验。**

### 第1步：安装Python
[python.org/downloads](https://www.python.org/downloads/) → 一定要勾选 **"Add Python to PATH"**

### 第2步：下载项目
```
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

### 第3步：安装依赖包
```
pip install -r requirements.txt
```

### 第4步：获取API密钥（免费）
从上表选择一个平台 → 复制密钥

### 第5步：设置API密钥
将 `.env.example` 复制为 `.env` → 用记事本打开 → 输入密钥

### 第6步：启动应用
```
streamlit run app.py
```
浏览器自动打开 **http://localhost:6601**。

---

## 使用方法

| 操作 | 方法 |
|------|------|
| 添加新闻来源 | 侧边栏 → 来源管理 |
| 追踪关键词 | 侧边栏 → 监控列表 |
| 收藏文章 | 新闻选项卡 → 点击☆ |
| 添加备注 | 书签选项卡 → 输入备注 |
| 搜索文章 | 搜索选项卡 → 关键词+过滤器 |
| 向AI提问 | AI聊天选项卡 → 输入问题 |
| 导出PDF | 简报/新闻选项卡 → 选择PDF |
| 切换暗色/亮色 | 侧边栏顶部切换按钮 |
| 更改LLM | `.env`中设置 `LLM_PROVIDER=groq` |

---

## 故障排除

| 问题 | 解决方法 |
|------|---------|
| 找不到 `pip` | 重新安装Python，勾选"Add to PATH" |
| "LLM API密钥未设置"警告 | 在`.env`中至少输入一个API密钥 |
| 没有文章显示 | 先点击"收集"→ 再点击"AI处理" |
| 端口被占用 | 使用 `--server.port 6602` 选项 |
| PDF失败 | 仅Windows可用（使用韩语字体） |

---

## 路线图

| Phase | 功能 | 状态 |
|-------|------|------|
| Phase 1 | 收集+AI摘要+仪表板（17项） | **已完成** |
| Phase 2-A | 搜索+书签+已读+情感图表+AI聊天（5项） | **已完成** |
| Phase 2-B | 语音+Telegram机器人+事实核查+术语表+GitHub Actions（5项） | **已完成** |
| Phase 3 | 智能体+预测+播客+插件+团队模式 | 计划中 |

---

## 许可证

MIT License - Copyright (c) 2026 **SoDam AI Studio**

详情请参阅 [LICENSE](./LICENSE) 文件。

---

*使用 Streamlit + 35个AI平台构建 — SoDam AI Studio*
