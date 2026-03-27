<div align="center">

# AI News Radar

**Your AI-powered news intelligence platform — auto-collects, analyzes, and delivers AI news from 74 sources with 35 LLM support.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.44+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![LLMs](https://img.shields.io/badge/LLM_Platforms-35-blueviolet)](#35-llm-platforms)
[![Sources](https://img.shields.io/badge/News_Sources-74-blue)](#74-news-sources)
[![Commits](https://img.shields.io/badge/Commits-37-orange)](#)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

**Language** &nbsp;/&nbsp; [Korean](./README_KO.md) &nbsp;/&nbsp; [Japanese](./README_JA.md) &nbsp;/&nbsp; [Chinese](./README_ZH.md)

</div>

---

## Why AI News Radar?

The AI landscape changes by the hour. New models drop, tools update, papers publish, and companies pivot — all across dozens of scattered sources. **AI News Radar** eliminates the noise. It continuously collects news from **74 curated sources**, uses AI to summarize, categorize, score, and fact-check every article, then delivers a clean, actionable briefing — in your language, on your schedule, across your preferred platforms.

**In one sentence:** Stop visiting 74 sites. Let AI read them all and tell you what matters.

---

## Highlights

- **50+ features** across 5 tabs (Dashboard / News Feed / AI / Insights / Share)
- **74 sources** — General AI (26) + Image & Video (20) + Vibe Coding (19) + Ontology (9)
- **35 LLM platforms** — most with free tiers, only one API key needed
- **9 categories** — Tools, Research, Trends, Tutorials, Business, Image/Video, Vibe Coding, Ontology, Other
- **19 tracked AI tools** with automatic release detection
- **5 SNS platforms** — X, Telegram, Discord, Threads, Instagram + auto-generated card news
- **5 content types** — Tweet, Thread, Instagram caption, Blog post, LinkedIn post
- **Voice briefing**, AI fact-check, AI glossary, AI debate
- **One-click full pipeline** — Collect > Analyze > Brief > Detect releases
- **Desktop app** with system tray + background notifications
- **GitHub Actions** — automated collection 3 times daily
- **Auto Korean translation** (English to Korean)

---

## Features (50+)

### Dashboard Tab

| Feature | Description |
|---------|-------------|
| Daily Briefing | AI-generated "Top 5 AI News Today" with importance ranking |
| Focus Briefing | Dedicated briefings for Image/Video, Vibe Coding, and Ontology |
| Category Quick Filter | One-click filter across 9 categories |
| Sentiment Gauge | Interactive Plotly charts showing positive / neutral / negative ratio |
| Voice Briefing | Listen to briefings as AI-generated speech via edge-tts |
| Weekly Intelligence Report | Auto-generated weekly report with trends, predictions, and analysis |
| Newsletter | Send daily or weekly briefings via email (SMTP) |

### News Feed Tab

| Feature | Description |
|---------|-------------|
| 74-Source Collection | Parallel crawling with 15 workers for fast aggregation |
| AI Summary | 3-line Korean summary for every article |
| 9-Category Classification | Automatic categorization with AI |
| Importance Scoring | 1–5 star rating per article |
| Sentiment Analysis | Positive / Neutral / Negative tagging |
| AI Fact-Check | Cross-source verification ("3 outlets confirmed" vs "single source") |
| Duplicate Merging | Same story from multiple outlets merged automatically |
| Keyword Watchlist | Highlight and alert on your tracked keywords |
| In-App Reader | Read full articles inside the dashboard (ad-free) |
| Advanced Search | Filter by keyword, category, sentiment, and read status |
| Bookmarks + Memo | Save articles with personal notes |
| Pagination | 10 articles per page with smooth navigation |
| Timeline View | Browse by Today / Yesterday / This Week |
| Auto Korean Translation | English articles translated to Korean automatically |

### AI Tab

| Feature | Description |
|---------|-------------|
| AI News Chat | Ask natural-language questions about collected news |
| AI Glossary | Auto-extracted AI terms with beginner-friendly explanations |

### Insights Tab

| Feature | Description |
|---------|-------------|
| AI Tool Release Tracker | Track 19 AI tools with automatic release detection |
| Trend Charts | Daily mention frequency with interactive Plotly line charts |
| Hot Keywords | Rising keywords with week-over-week change rate |
| AI Debate | "Midjourney vs Flux" — AI generates pros, cons, and verdict |
| Weekly Intelligence Report | Deep-dive weekly analysis with predictions |

### Share Tab

| Feature | Description |
|---------|-------------|
| SNS Auto-Post | Post to X, Telegram, Discord, Threads, and Instagram |
| Card News Generator | Auto-generate 1080×1080 card images (dark theme, per-category colors) |
| AI Content Generation | Auto-generate tweets, threads, Instagram captions, blog posts, LinkedIn posts |
| Newsletter Email | Send formatted briefings to subscriber lists |
| Export | Download as Markdown or PDF |

### System Features

| Feature | Description |
|---------|-------------|
| One-Click Full Pipeline | Collect > AI Process > Briefing > Release Detection in one click |
| Parallel Crawling | 15 concurrent workers for fast collection |
| Batch Parallel Processing | Efficient batch AI processing for large article sets |
| Smart Keyword Alert | Desktop notification when watched keywords appear |
| Desktop App | Native window via pywebview + system tray + background mode |
| GitHub Actions | Automated collection 3 times daily (configurable) |
| Telegram Bot | 7 commands for on-the-go access |

---

## 74 News Sources

| Category | Count | Examples |
|----------|:-----:|---------|
| **General AI** | 26 | TechCrunch, The Verge, MIT Tech Review, Wired, ZDNET, Ben's Bites, Ars Technica |
| **Image & Video** | 20 | Stability AI, Civitai, Runway, Reddit (StableDiffusion, midjourney, flux_ai, comfyui) |
| **Vibe Coding** | 19 | Cursor, GitHub, Anthropic, Simon Willison, Reddit (vibecoding, ClaudeAI, cursor) |
| **Ontology** | 9 | Neo4j, Stardog, W3C, Reddit (semanticweb, KnowledgeGraphs) |

---

## 35 LLM Platforms

You only need **one API key** from any platform below:

| Tier | Platforms |
|------|-----------|
| **Free (Recommended)** | Gemini, Groq, Cerebras, SambaNova, xAI, Mistral, Cohere, HuggingFace, NVIDIA, Cloudflare, Zhipu, Kluster, GLHF, Hyperbolic |
| **Credits / Budget** | Together AI, OpenRouter, Fireworks, DeepSeek, DeepInfra, Perplexity, AI21, Upstage, Lepton, Novita, Nebius, Chutes, Replicate, Alibaba, Moonshot, Yi, Baichuan |
| **Premium** | OpenAI, Azure OpenAI, Anthropic Claude, Reka AI |

> **Tip:** Gemini and Groq are the easiest to set up with generous free tiers.

---

## Dashboard Overview (5 Tabs)

| Tab | What's Inside |
|-----|---------------|
| **Dashboard** | Daily briefing, Focus briefings, Category quick filter, Sentiment charts, Weekly report, Newsletter |
| **News Feed** | All news, Advanced search, Bookmarks, Timeline view, Pagination |
| **AI** | News chat, AI glossary |
| **Insights** | Release tracker, Trend charts, Hot keywords, AI debate, Weekly report |
| **Share** | SNS posting, AI content generation, Card news, Newsletter, Export |

---

## Getting Started (7-Step Beginner Guide)

> **Zero coding experience needed.** Follow each step carefully.

### Step 1 — Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow **"Download Python"** button
3. Run the downloaded file
4. **CRITICAL:** Check the **"Add Python to PATH"** checkbox at the bottom of the installer
5. Click **"Install Now"**

**Verify installation:** Open a terminal (`Win + R` > type `cmd` > Enter) and run:

```bash
python --version
```

You should see `Python 3.11.x` or higher.

### Step 2 — Download the Project

**Option A: Using Git (recommended)**

```bash
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**Option B: Direct download**

1. Go to the [GitHub repository](https://github.com/sodam-ai/ai-news-radar)
2. Click the green **"Code"** button > **"Download ZIP"**
3. Extract the ZIP to a folder of your choice
4. Open a terminal in that folder

### Step 3 — Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages. Wait until the process completes (may take 1–2 minutes).

### Step 5 — Get a Free API Key

Choose **any one** platform. We recommend **Groq** for the fastest setup:

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up with a Google account (takes 10 seconds)
3. Click **"Create API Key"**
4. Copy the key (starts with `gsk_`)

> Other free options: [Gemini](https://aistudio.google.com/apikey), [Cerebras](https://cloud.cerebras.ai/), [SambaNova](https://cloud.sambanova.ai/)

### Step 6 — Configure Your API Key

1. Find the file `.env.example` in the project folder
2. Copy it and rename the copy to `.env`
3. Open `.env` with any text editor (Notepad works fine)
4. Paste your API key:

```env
# Pick one (or more):
GROQ_API_KEY=gsk_YourActualKeyHere
# GEMINI_API_KEY=your_gemini_key
# OPENAI_API_KEY=sk-your_openai_key
```

5. Save and close the file

> **Security note:** The `.env` file is listed in `.gitignore` and will never be uploaded to GitHub. Never share this file publicly.

### Step 7 — Launch the App

**Web mode (opens in your browser):**

```bash
streamlit run app.py
```

Your browser opens to **http://localhost:6601**

**Desktop mode (native window):**

```bash
python desktop.py
```

Or double-click **`AI_News_Radar.bat`** on Windows.

### First Use

1. Click **"Collect"** in the sidebar — gathers news from 74 sources (~1 min)
2. Click **"AI Process"** — AI analyzes, summarizes, and categorizes all articles
3. Click **"Generate Briefing"** — creates today's Top 5 briefing
4. Explore the 5 tabs and discover all features!

---

## Usage Guide

| What You Want | How to Do It |
|---------------|--------------|
| Read today's summary | Dashboard tab > Briefing section |
| Filter by category | Dashboard tab > Click any category quick filter |
| Search for a topic | News Feed tab > Search view > Enter keyword |
| Ask AI about news | AI tab > Chat view > Type your question |
| Learn an AI term | AI tab > Glossary view > Browse or search |
| Track AI tool releases | Insights tab > Release Tracker |
| See trending keywords | Insights tab > Trends |
| Run an AI debate | Insights tab > AI Debate > Pick two tools |
| Generate SNS content | Share tab > Content Generation > Select article + platform |
| Post to social media | Share tab > SNS Posting > Select platforms > Post |
| Listen to briefing | Dashboard tab > Select voice > Click "Voice" |
| Export as PDF | Share tab > Export view |
| Save an article | News Feed tab > Click bookmark icon on any article |
| Set keyword alerts | Sidebar > Watchlist > Enter keyword |
| Run full pipeline | Sidebar > "One-Click Pipeline" button |

---

## SNS Platform Setup

| Platform | Setup Time | Difficulty | Guide |
|----------|:----------:|:----------:|-------|
| Discord | 30 sec | Very Easy | Create webhook URL in channel settings |
| Telegram | 2 min | Easy | Create bot via @BotFather |
| X (Twitter) | 10 min | Medium | Apply for developer account |
| Threads | 10 min | Medium | Meta developer portal |
| Instagram | 15 min | Complex | Instagram Graph API setup |

Detailed step-by-step instructions are available in the **Share tab > SNS Posting** section within the app.

---

## Project Structure

```
ai-news-radar/
├── app.py                       # Main dashboard (5 tabs)
├── desktop.py                   # Desktop app (pywebview + system tray)
├── config.py                    # Settings (9 categories, ports, paths)
├── requirements.txt             # Required packages
├── .env.example                 # API key template
├── AI_News_Radar.bat            # Windows launcher (web mode)
├── AI_News_Radar_Silent.vbs     # Silent launcher (no console window)
│
├── ai/                          # 14 AI modules
│   ├── model_router.py          #   35 LLM provider routing
│   ├── briefing.py              #   Daily + focus briefing generation
│   ├── chat.py                  #   Natural-language news chat
│   ├── voice_briefing.py        #   TTS voice output (edge-tts)
│   ├── factcheck.py             #   Cross-source fact verification
│   ├── glossary.py              #   AI terminology dictionary
│   ├── weekly_report.py         #   Weekly intelligence report
│   ├── competitor.py            #   AI tool release monitoring
│   ├── release_tracker.py       #   Automatic release detection
│   ├── trend.py                 #   Keyword trend analysis
│   ├── debate.py                #   AI debate mode
│   ├── smart_alert.py           #   Desktop keyword notifications
│   ├── translator.py            #   Auto Korean translation
│   ├── deduplicator.py          #   Duplicate article merging
│   └── batch_processor.py       #   Batch parallel processing
│
├── sns/                         # SNS & sharing modules
│   ├── card_generator.py        #   1080×1080 card news images (Pillow)
│   ├── poster.py                #   5-platform SNS posting
│   ├── content_generator.py     #   AI content (5 types)
│   └── newsletter.py            #   Email newsletter (SMTP)
│
├── crawler/                     # Data collection
│   ├── rss_crawler.py           #   RSS feed crawler (15 parallel workers)
│   └── scheduler.py             #   APScheduler-based scheduling
│
├── bot/                         # Telegram integration
│   └── telegram_bot.py          #   Telegram bot (7 commands)
│
├── reader/                      # Article reading
│   └── article_reader.py        #   Ad-free in-app article reader
│
├── export/                      # Data export
│   └── exporter.py              #   Markdown + PDF export
│
├── utils/                       # Shared utilities
│   └── helpers.py               #   Common helper functions
│
├── scripts/                     # CLI tools
│   ├── collect.py               #   Standalone collection script
│   └── reclassify.py            #   Category reclassification tool
│
├── data/                        # Local data storage
│   ├── preset_sources.json      #   74 curated source definitions
│   ├── sources.json             #   Active source configuration
│   ├── articles.json            #   Collected articles
│   ├── briefings.json           #   Generated briefings
│   ├── weekly_reports.json      #   Weekly report archive
│   ├── release_log.json         #   Tool release history
│   ├── audio/                   #   Voice briefing audio files
│   └── cards/                   #   Generated card news images
│
├── .github/workflows/
│   └── collect.yml              #   GitHub Actions (3× daily auto-collect)
│
└── PRD/                         #   Product design documents
```

**24 modules** across 8 directories — **37 commits** and counting.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.11+ |
| **Dashboard** | Streamlit 1.44+ |
| **AI Engine** | 35 LLM platforms via unified model router |
| **Charts** | Plotly (interactive trend charts, sentiment gauges) |
| **Voice** | edge-tts (Microsoft neural TTS) |
| **Image Generation** | Pillow (card news with dark theme) |
| **Desktop** | pywebview + pystray (native window + system tray) |
| **Notifications** | plyer (cross-platform desktop alerts) |
| **RSS Parsing** | feedparser (74 source feeds) |
| **Web Scraping** | BeautifulSoup4 + requests |
| **Telegram Bot** | python-telegram-bot |
| **SNS APIs** | tweepy (X), Telegram API, Discord Webhook, Threads API, Instagram Graph API |
| **Email** | smtplib (SMTP newsletter) |
| **PDF Export** | fpdf2 (Korean font support) |
| **Scheduling** | APScheduler (in-app), GitHub Actions (CI/CD) |
| **Data Storage** | Local JSON (zero database setup) |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `python` not found | Reinstall Python with **"Add to PATH"** checked |
| `pip` not found | Try `python -m pip install -r requirements.txt` instead |
| `streamlit` not found | Run `pip install streamlit` or check your virtual environment is activated |
| "API key not set" warning | Create a `.env` file with at least one API key (see Step 6) |
| No articles appear | Click **"Collect"** first, then **"AI Process"** |
| Categories show 0 articles | Run `python scripts/reclassify.py` to reclassify existing articles |
| Port 6601 already in use | Use `streamlit run app.py --server.port 7777` |
| PDF export fails on macOS/Linux | PDF export uses Windows Korean fonts; install `NanumGothic` font |
| Desktop mode won't launch | Ensure `pywebview` is installed: `pip install pywebview` |
| Slow collection | Normal — 74 sources with 15 parallel workers takes ~60 seconds |
| Edge-tts voice error | Check internet connection; edge-tts requires online access |

---

## Roadmap

| Phase | Features | Status |
|-------|----------|:------:|
| **Phase 1** | Collection + AI Summary + Dashboard (17 features) | ✅ Done |
| **Phase 2-A** | Search + Bookmarks + Sentiment + Chat (5 features) | ✅ Done |
| **Phase 2-B** | Voice + Telegram + Fact-check + Glossary + Actions (5 features) | ✅ Done |
| **Tier 1** | Focus Briefing + Weekly Report + Release Tracker (3 features) | ✅ Done |
| **Tier 2** | Trend Charts + AI Debate + Hot Keywords (3 features) | ✅ Done |
| **S-Tier** | Smart Alert + Content Gen + Newsletter + SNS (4 features) | ✅ Done |
| **UI/UX** | 5-tab redesign + Pagination + Category Quick Filter + Premium CSS | ✅ Done |
| **Desktop** | pywebview + System Tray + Background Notifications | ✅ Done |
| **Pipeline** | One-Click Full Pipeline + Parallel Crawling + Batch Processing | ✅ Done |
| **Translation** | Auto Korean Translation + Deduplication | ✅ Done |
| **Next** | ChromaDB vector search, Ollama local LLM, Gamification, Mobile PWA | 📋 Planned |

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License — Copyright (c) 2026 **SoDam AI Studio**

See [LICENSE](./LICENSE) for details.

---

<div align="center">

*Built with Streamlit + 35 AI Platforms by SoDam AI Studio*

</div>
