# 📡 AI News Radar

<p align="center">
  <img src="assets/icon.png" width="80" alt="AI News Radar Icon" />
</p>

<p align="center">
  <strong>Your Personal AI News Intelligence Platform</strong><br/>
  Automatically collect, summarize, and analyze AI news from 74 sources
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License"/>
  <img src="https://img.shields.io/badge/Release-v1.6.0-blue" alt="Release"/>
  <img src="https://img.shields.io/badge/Streamlit-1.44%2B-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/LLM-39_Providers_(Local_4_+_Cloud_35)-purple" alt="LLM"/>
  <img src="https://img.shields.io/badge/Vector_Search-ChromaDB-orange" alt="ChromaDB"/>
</p>

<p align="center">
  <a href="README.md">한국어</a> |
  <a href="README_EN.md">English</a>
</p>

---

## What is AI News Radar?

A personal AI news tool that **requires zero coding experience** to use.

- 📰 **74 AI news sources** — automatically collects the latest news
- 🤖 **AI-powered processing** — auto-summarizes, categorizes, scores importance, and analyzes sentiment
- 📋 **Daily TOP 5 briefing** — generated automatically every day
- 💬 **Natural language Q&A** — just ask: "What happened with Claude this week?"
- 🔍 **Semantic search** — finds related articles even without exact keyword matches (ChromaDB + ONNX)
- ⭐ **Bookmarks + notes** — save and annotate important articles
- 📱 **Telegram bot** — get important news alerts without opening the app
- 📊 **Trend & competitor analysis** — visualize AI industry movements at a glance

> Runs **100% locally** on your machine. Your data never leaves your computer.

---

## Quick Start (No Coding Experience Needed)

### Step 1: Install Python

Skip to Step 2 if Python is already installed.

1. Go to **[python.org/downloads](https://www.python.org/downloads/)** in your browser
2. Click the yellow **"Download Python 3.xx"** button
3. Run the downloaded installer
4. **IMPORTANT**: Check **"Add Python to PATH"** at the bottom of the installer screen
5. Click **"Install Now"** → click "Close" when done

### Step 2: Download the App

**Option A — GitHub Releases (recommended):**
1. Visit the [Releases page](https://github.com/sodam-ai/ai-news-radar/releases)
2. Download **`Source code (zip)`**
3. Right-click the ZIP → "Extract All" → choose a folder → "Extract"

**Option B — From this page:**
1. Click the green **"Code"** button at the top
2. Click **"Download ZIP"**
3. Extract the ZIP to any folder

### Step 3: Get a Free API Key (30 seconds)

AI News Radar uses AI to analyze news. You'll need a free API key.

1. Go to **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIzaSy...`)

> **Is it really free?** Yes! Google provides 1,000 free requests per day — more than enough for personal news tracking. No credit card required.

### Step 4: Create the Config File

Inside the downloaded folder:

1. Find the `.env.example` file and copy it
2. Rename the copy to `.env`
3. Open `.env` in Notepad
4. Paste your API key after `GEMINI_API_KEY=`

```
GEMINI_API_KEY=AIzaSyPasteYourKeyHere
```

Save and close.

### Step 5: Run the App

**Double-click to launch:**
- Double-click `AI_News_Radar.exe` — it will auto-install packages and launch
- First launch may take 2–3 minutes for package installation
- Your browser will automatically open `http://localhost:6601`

**Or use the batch file:**
- Double-click `AI_News_Radar.bat`

---

## Full Feature List

| Feature | Description |
|---------|-------------|
| 📡 Auto Collection | 74 RSS sources fetched in parallel (15 threads) |
| 🤖 AI Batch Processing | Summary, category, importance, sentiment, keywords — all at once |
| 🔍 Semantic Search | ChromaDB + ONNX local embedding (new in v1.3.0) |
| 💬 AI Chat | Natural language conversation over collected news |
| 📋 Daily Briefing | TOP 5 auto-generated each day |
| 📊 Weekly Report | Trend & forecast PDF auto-generated |
| ⭐ Bookmarks + Notes | Save and annotate articles |
| 🔔 Smart Alerts | Desktop notification when watchlist keywords appear |
| 📱 Telegram Bot | `/today`, `/ask`, `/alert`, `/bookmark` |
| 🌐 Translation | Auto-translate English articles to Korean |
| 🎙️ Voice Briefing | edge-tts AI voice reads the briefing aloud |
| 📈 Trend Charts | Time-series keyword mention analysis |
| 🏢 Competitor Tracking | Monitor AI companies and products |
| ✅ Fact-Check Badge | Credibility score based on number of sources reporting |
| 🗣️ Debate Mode | AI auto-generates pro/con perspectives |
| 📚 AI Glossary | Auto-extracts and explains technical terms from news |
| 🚀 Release Tracker | Detects new versions of AI tools automatically |
| 📤 Export | Markdown and PDF export |
| 📲 Social Cards | Auto-generate shareable news cards |
| 🤖 35 LLM Providers | Gemini, Claude, GPT, Groq, and more — auto-switching |

---

## Environment Variables (.env)

Configure in the `.env` file. Only one API key is required to get started.

```env
# ── Required (only one needed) ────────────────────
GEMINI_API_KEY=AIzaSy...          # Google AI Studio (free: 1,000 req/day)

# ── Optional: Additional LLM Providers ────────────
GROQ_API_KEY=gsk_...              # Groq (free: 14,400 req/day, very fast)
OPENAI_API_KEY=sk-...             # OpenAI GPT
ANTHROPIC_API_KEY=sk-ant-...      # Anthropic Claude

# ── Optional: Telegram Bot ─────────────────────────
TELEGRAM_BOT_TOKEN=123456:ABC...  # Get from @BotFather
TELEGRAM_CHAT_ID=123456789        # Get from @userinfobot

# ── Optional: Crawl Schedule ──────────────────────
CRAWL_INTERVAL_MINUTES=60         # Default: auto-collect every 60 minutes
```

> **Security notice**: Never share your `.env` file. It is already listed in `.gitignore` and will not be uploaded to GitHub.

---

## Telegram Bot Setup

1. Search **@BotFather** in Telegram
2. Send `/newbot` → set a name → copy the token
3. Add `TELEGRAM_BOT_TOKEN=your_token` to `.env`
4. Search **@userinfobot** in Telegram → send `/start` → copy your numeric ID
5. Add `TELEGRAM_CHAT_ID=your_id` to `.env`
6. Run in terminal: `python -m bot.telegram_bot`

**Bot Commands:**
| Command | Description |
|---------|-------------|
| `/today` | Today's AI briefing |
| `/top` | Top 5 most important news |
| `/search keyword` | Search news |
| `/ask question` | Ask AI about the news |
| `/alert` | View watchlist keywords |
| `/alert keyword` | Add keyword to watchlist |
| `/bookmark` | View bookmarked articles |
| `/stats` | Collection statistics |

---

## Semantic Search Setup (New in v1.3.0)

After first launch, click the **"🧠 Vector Sync"** button in the sidebar once.  
This registers existing articles into the AI search database. After that, it's automatic.

---

## Folder Structure

```
ai-news-radar/
├── app.py                  # Main Streamlit dashboard (~1,400 lines)
├── config.py               # Settings (port, categories, API key loading)
├── requirements.txt        # Package list
├── .env                    # API keys (create yourself, not on GitHub)
├── .env.example            # Example environment file
│
├── ai/                     # AI processing modules
│   ├── model_router.py     # 35-provider LLM routing
│   ├── batch_processor.py  # Batch AI analysis
│   ├── vector_store.py     # ChromaDB semantic search (v1.3.0)
│   ├── chat.py             # AI news chat
│   ├── briefing.py         # Daily briefing generation
│   ├── weekly_report.py    # Weekly report
│   ├── trend.py            # Trend analysis
│   ├── competitor.py       # Competitor monitoring
│   ├── smart_alert.py      # Smart alerts (Telegram integration)
│   ├── factcheck.py        # Fact-check badge
│   ├── debate.py           # Debate mode
│   ├── glossary.py         # AI glossary
│   ├── release_tracker.py  # Release detection
│   ├── translator.py       # EN→KR auto translation
│   ├── voice_briefing.py   # Voice briefing
│   └── deduplicator.py     # Duplicate article merging
│
├── crawler/                # News collection
│   ├── rss_crawler.py      # Multi-threaded RSS crawler (74 sources)
│   └── scheduler.py        # Auto-crawl scheduler
│
├── bot/                    # Telegram bot
│   └── telegram_bot.py     # Bot command handlers
│
├── sns/                    # Social media
│   ├── card_generator.py   # News card generator
│   ├── content_generator.py
│   ├── newsletter.py       # Email newsletter
│   └── poster.py           # Social posting
│
├── reader/                 # Article reader
│   └── article_reader.py   # Clean article view
│
├── export/                 # Export
│   └── exporter.py         # Markdown/PDF export
│
├── utils/                  # Common utilities
│   ├── helpers.py          # JSON read/write, logging, etc.
│   └── bookmarks.py        # Bookmark management (v1.3.0)
│
└── data/                   # Runtime data (auto-created, excluded from Git)
    ├── articles.json        # Collected articles
    ├── sources.json         # Registered sources
    ├── briefings.json       # Generated briefings
    ├── chroma/              # Vector search database
    └── audio/               # Voice briefing files
```

---

## Operational Notes

| Topic | Details |
|-------|---------|
| **API Keys** | Keep in `.env` only. Never share via GitHub, email, or chat |
| **API Limits** | Gemini Flash free tier: 250 req/day. Automatically switches to Groq or others if exceeded |
| **data/ folder** | Articles accumulate over time — periodic cleanup recommended |
| **Port conflict** | If port `6601` is in use, change it in `.env` |
| **Vector sync** | Delete `data/chroma/` and re-sync to reset the vector database |
| **Telegram alerts** | Without `TELEGRAM_CHAT_ID` in `.env`, only desktop notifications are sent |

---

## Version History

| Version | Changes |
|---------|---------|
| v1.3.0 | ChromaDB semantic search, Telegram bot enhancements (`/alert`, `/bookmark`), smart alert Telegram integration |
| v1.2.1 | Expanded multi-LLM support to 35 providers |
| v1.2.0 | Lightweight exe launcher (7.8 MB), multi-resolution icons |
| v1.0.0 | MVP release — collection, summarization, categorization, briefing, chat |

---

## License

MIT License © 2026 [SoDam AI Studio](https://github.com/sodam-ai)

Free to use, modify, and distribute.  
For commercial use, please keep the original attribution.
