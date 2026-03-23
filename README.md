# AI News Radar

> **Your personal AI news dashboard that automatically collects, summarizes, and categorizes AI news — with 35 LLM platform support.**

**Language / [Korean](./README_KO.md) / [Japanese](./README_JA.md) / [Chinese](./README_ZH.md)**

---

## What is AI News Radar?

AI News Radar is a **personal dashboard** that automatically gathers AI-related news from around the world, then uses AI to summarize, categorize, and rank them by importance. It supports **35 LLM platforms** including OpenAI, Gemini, Groq, Claude, and many more — most with free tiers.

**In simple terms:** Instead of visiting 15+ news sites every day, this app does it for you and shows you only what matters.

---

## Key Features (27 features)

### Phase 1 — Core (17 features)

| Feature | Description |
|---------|-------------|
| Auto-Collect | Automatically gathers news from 15 pre-set sources (TechCrunch, The Verge, MIT Tech Review, etc.) |
| AI Summary | Summarizes each article into 3 lines in Korean |
| Smart Categorization | Sorts news into 6 categories: Tools, Research, Trends, Tutorials, Business, Other |
| Importance Score | Rates each article from 1 to 5 stars |
| Sentiment Analysis | Tags each article as Positive / Neutral / Negative |
| Daily Briefing | Generates a "Top 5 AI News Today" briefing every day |
| Duplicate Merging | When multiple outlets cover the same story, merges them into one |
| Keyword Watchlist | Highlights news containing your tracked keywords (e.g., "Claude", "GPT") |
| In-App Reader | Read full articles inside the dashboard without ads |
| Dark Mode | Switch between dark and light themes |
| Export (Markdown) | Download briefings and articles as Markdown |
| Export (PDF) | Download briefings and articles as PDF with Korean font support |
| Image Analysis | AI analyzes charts and infographics found in news articles |
| Live Updates | Dashboard refreshes automatically every 5 minutes |
| Timeline View | Browse news chronologically (Today / Yesterday / This Week) |
| Context Caching | Caches system prompts to reduce API token costs |
| Smart Routing | Uses lighter model for simple tasks, stronger model for complex tasks |

### Phase 2-A — Enhanced (5 features)

| Feature | Description |
|---------|-------------|
| Search | Search articles by keyword + category + sentiment + read status |
| Bookmarks + Memo | Save important articles with personal notes |
| Read History | Mark articles as read, filter unread articles |
| Sentiment Gauge | Plotly charts: gauge (positive %), donut (distribution), stacked bar (by category) |
| AI Chat | Ask questions about collected news in natural language |

### Phase 2-B — Advanced (5 features)

| Feature | Description |
|---------|-------------|
| Voice Briefing | Listen to daily briefing as AI-generated Korean speech (edge-tts, male/female voices) |
| AI Fact-Check | Cross-reference badge: "✅ Confirmed by N outlets" vs "⚠️ Single source" |
| AI Glossary | Auto-extract AI terms from news + beginner-friendly explanations (difficulty/category filters) |
| Telegram Bot | `/today` briefing, `/top` news, `/search`, `/ask` AI chat — all from Telegram |
| GitHub Actions | Auto-collect 3x daily (06/12/18 KST), manual dispatch, CLI script |

---

## 35 LLM Platforms Supported

You only need **one API key** from any of these platforms:

### Free Tier (Recommended)

| Platform | Free Quota | Get Key |
|----------|-----------|---------|
| Google Gemini | Flash-Lite 1,000/day, Flash 250/day | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| Groq | 30/min, 14,400/day | [console.groq.com/keys](https://console.groq.com/keys) |
| Cerebras | 30/min (ultra-fast) | [cloud.cerebras.ai](https://cloud.cerebras.ai/) |
| SambaNova | 10/min | [cloud.sambanova.ai](https://cloud.sambanova.ai/) |
| xAI (Grok) | $25/month free | [console.x.ai](https://console.x.ai/) |
| Mistral AI | Free experimental API | [console.mistral.ai](https://console.mistral.ai/api-keys) |
| Cohere | 1,000/month | [dashboard.cohere.com](https://dashboard.cohere.com/api-keys) |
| HuggingFace | Free (rate limited) | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| NVIDIA NIM | 1,000 credits | [build.nvidia.com](https://build.nvidia.com/) |
| Cloudflare Workers AI | 10,000 neurons/day | [dash.cloudflare.com](https://dash.cloudflare.com/) |
| Zhipu AI (GLM) | Flash model free | [open.bigmodel.cn](https://open.bigmodel.cn/) |
| Kluster AI | Free tier | [kluster.ai](https://kluster.ai/) |
| GLHF.chat | Free (community) | [glhf.chat](https://glhf.chat/) |
| Hyperbolic | Free tier | [app.hyperbolic.xyz](https://app.hyperbolic.xyz/) |

### Sign-up Credits / Affordable

| Platform | Credits | Get Key |
|----------|---------|---------|
| Together AI | $5 credit | [api.together.xyz](https://api.together.xyz/settings/api-keys) |
| OpenRouter | Some free models | [openrouter.ai/keys](https://openrouter.ai/keys) |
| Fireworks AI | $1 credit | [fireworks.ai](https://fireworks.ai/account/api-keys) |
| DeepSeek | $0.27/1M tokens | [platform.deepseek.com](https://platform.deepseek.com/api_keys) |
| DeepInfra | Free credits | [deepinfra.com](https://deepinfra.com/dash/api_keys) |
| Perplexity AI | $5 credit (with search) | [perplexity.ai](https://www.perplexity.ai/settings/api) |
| AI21 Labs | Free credits | [studio.ai21.com](https://studio.ai21.com/account/api-key) |
| Upstage (Solar) | Free credits (Korean) | [console.upstage.ai](https://console.upstage.ai/) |
| + 9 more | See .env.example | Various |

### Premium

| Platform | Pricing | Get Key |
|----------|---------|---------|
| OpenAI | $5 credit (new users) | [platform.openai.com](https://platform.openai.com/api-keys) |
| Azure OpenAI | $200 credit (free account) | [portal.azure.com](https://portal.azure.com/) |
| Anthropic Claude | Paid | [console.anthropic.com](https://console.anthropic.com/settings/keys) |
| Reka AI | Free credits | [platform.reka.ai](https://platform.reka.ai/) |

---

## Dashboard (8 Tabs)

| Tab | Description |
|-----|-------------|
| **Briefing** | Today's Top 5 + Sentiment Gauge + Voice Briefing (MP3) |
| **News** | All articles + filters + bookmark/read + fact-check badges |
| **Search** | Keyword + category + sentiment + read status filters |
| **AI Chat** | Ask questions about news in natural language |
| **Glossary** | AI term dictionary with beginner-friendly explanations |
| **Timeline** | Chronological news flow (Today / Yesterday / This Week) |
| **Bookmarks** | Saved articles with memo editing |
| **Sources** | Manage 15 news sources |

---

## Getting Started (Step-by-Step for Beginners)

> **You don't need any coding experience.** Just follow each step carefully.

### Step 1: Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow **"Download Python 3.xx"** button
3. Run the downloaded file
4. **IMPORTANT:** Check the box **"Add Python to PATH"** at the bottom
5. Click **"Install Now"**

**Verify:** Open Command Prompt (`Win + R` → `cmd` → Enter) and type:
```
python --version
```

### Step 2: Download This Project

**Option A: Using Git**
```
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**Option B: Direct Download** — Go to [GitHub page](https://github.com/sodam-ai/ai-news-radar) → Code → Download ZIP → Extract

### Step 3: Install Packages

```
cd path\to\ai-news-radar
pip install -r requirements.txt
```

### Step 4: Get an API Key (Free)

Choose **any one** platform from the table above. Example with Groq (easiest free option):

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up and create an API key
3. Copy the key

### Step 5: Set Up Your API Key

1. Copy `.env.example` to `.env`
2. Open `.env` with Notepad
3. Add your key:

```
GROQ_API_KEY=gsk_YourActualKeyHere
```

Or if using OpenAI:
```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-YourActualKeyHere
```

> **Security:** `.env` is automatically excluded from GitHub. Never share it.

### Step 6: Run the App

```
streamlit run app.py
```

Browser opens to **http://localhost:6601** — Done!

---

## How to Use

### First Time

1. Click **"Collect"** in sidebar → gathers news from 15 sources
2. Click **"AI Process"** → AI analyzes all articles
3. Click **"Generate Briefing"** → creates today's Top 5

### Daily Use

- **Briefing tab** — quick overview + sentiment charts
- **News tab** — browse with filters, bookmark important articles
- **Search tab** — find specific topics
- **AI Chat tab** — ask "What are today's most important AI news?"
- **Bookmarks tab** — review saved articles with your notes

### Features Guide

| Action | How To |
|--------|--------|
| Add a news source | Sidebar → Source Management → Enter name & RSS URL |
| Track a keyword | Sidebar → Keyword Watchlist → Enter keyword |
| Bookmark an article | News tab → Click ☆ on article card |
| Add memo to bookmark | Bookmarks tab → Type in memo field |
| Mark as read | News tab → Click 📖 on article card |
| Search articles | Search tab → Enter keyword + select filters |
| Chat with AI | AI Chat tab → Type your question |
| Listen to briefing | Briefing tab → Select voice → Click "Generate Voice" |
| Look up AI terms | Glossary tab → Browse or search terms |
| Use Telegram bot | Set `TELEGRAM_BOT_TOKEN` in `.env` → Run `python -m bot.telegram_bot` |
| Export as PDF | Briefing/News tab → Select PDF → Download |
| Switch dark/light | Sidebar → Toggle at top |
| Change LLM provider | Edit `.env` → Set `LLM_PROVIDER=groq` (or any provider name) |

---

## Project Structure

```
ai-news-radar/
├── app.py                  # Main dashboard (8 tabs)
├── config.py               # Settings
├── requirements.txt        # Dependencies (10 packages)
├── .env.example            # API key template (35 platforms + Telegram)
├── LICENSE                 # MIT License (SoDam AI Studio)
├── .streamlit/config.toml  # Theme + port settings
├── crawler/
│   ├── rss_crawler.py      # RSS feed collection
│   └── scheduler.py        # Auto-collection scheduler
├── ai/
│   ├── model_router.py     # 35 LLM providers + smart routing
│   ├── batch_processor.py  # Batch AI processing + image analysis
│   ├── deduplicator.py     # Duplicate news merging
│   ├── briefing.py         # Daily Top 5 briefing
│   ├── chat.py             # AI news chat (keyword RAG)
│   ├── voice_briefing.py   # Voice briefing (edge-tts)
│   ├── factcheck.py        # Cross-source fact-check badges
│   └── glossary.py         # AI term dictionary
├── bot/
│   └── telegram_bot.py     # Telegram bot (7 commands)
├── scripts/
│   └── collect.py          # CLI collection script (for cron/Actions)
├── .github/workflows/
│   └── collect.yml         # GitHub Actions auto-collect (3x daily)
├── reader/
│   └── article_reader.py   # Ad-free article reader
├── export/
│   └── exporter.py         # Markdown + PDF export
├── data/
│   └── preset_sources.json # 15 pre-configured sources
├── utils/
│   └── helpers.py          # Utilities + safe logging
├── PRD/                    # Design documents
└── README*.md              # 4 languages (EN/KO/JA/ZH)
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `pip` not found | Reinstall Python, check "Add Python to PATH" |
| `streamlit` not found | Run: `pip install streamlit` |
| "LLM API key not set" warning | Create `.env` file with at least one API key |
| No articles appear | Click "Collect" first, then "AI Process" |
| Port 6601 in use | Change port in `.streamlit/config.toml` or use `--server.port 6602` |
| PDF export fails | Windows only (uses Windows Korean fonts) |
| AI analysis not working | Check API key in `.env` is correct and not expired |
| App crashes on startup | Run `pip install -r requirements.txt` again |
| Chat returns JSON instead of text | Already fixed — update to latest version |

---

## Roadmap

| Phase | Features | Status |
|-------|----------|--------|
| Phase 1 (MVP) | Collection + AI Summary + Dashboard (17 features) | **Complete** |
| Phase 2-A | Search + Bookmarks + Read History + Sentiment Chart + AI Chat (5 features) | **Complete** |
| Phase 2-B | Voice Briefing + Telegram Bot + Fact-check + Glossary + GitHub Actions (5 features) | **Complete** |
| Phase 3 | Agents + Prediction + Podcast + Plugins + Team mode | Planned |

See [PRD/03_PHASES.md](./PRD/03_PHASES.md) for the full roadmap.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| Dashboard | Streamlit 2026 |
| AI | 35 LLM platforms (OpenAI, Gemini, Groq, Claude, etc.) |
| Charts | Plotly (gauge, donut, stacked bar) |
| Data | Local JSON files |
| Scheduling | APScheduler |
| PDF | fpdf2 (Korean font support) |
| Voice | edge-tts (Microsoft TTS, Korean) |
| Bot | python-telegram-bot (Telegram integration) |
| CI/CD | GitHub Actions (auto-collect 3x daily) |

---

## License

MIT License - Copyright (c) 2026 **SoDam AI Studio**

See [LICENSE](./LICENSE) for details.

---

*Built with Streamlit + 35 AI Platforms by SoDam AI Studio*
