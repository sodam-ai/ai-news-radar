<div align="center">

# AI News Radar

**Your AI-powered news intelligence platform — auto-collects, analyzes, and delivers AI news from 74 sources with 35 LLM platform support.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.44+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![LLMs](https://img.shields.io/badge/LLM_Platforms-35-blueviolet)](#35-llm-platforms)
[![Sources](https://img.shields.io/badge/News_Sources-74-blue)](#74-news-sources)
[![License](https://img.shields.io/badge/License-SoDam_AI_Studio-green)](./LICENSE)

**Language** &nbsp;/&nbsp; [Korean 한국어](./README_KO.md) &nbsp;/&nbsp; [Japanese 日本語](./README_JA.md) &nbsp;/&nbsp; [Chinese 中文](./README_ZH.md)

</div>

---

## Why AI News Radar?

The AI landscape changes by the hour. New models drop, tools update, papers publish, and companies pivot — all across dozens of scattered sources. AI News Radar eliminates the noise. It continuously collects news from 74 curated sources, uses AI to summarize, categorize, score, and fact-check every article, then delivers a clean, actionable briefing — in your language, on your schedule.

**In one sentence:** Stop visiting 74 sites. Let AI read them all and tell you what matters.

---

## 🔒 Security & Privacy — Read This First

### Your API Key Is 100% Private — Never Uploaded

When you download this project, **it contains NO API keys, NO passwords, and NO personal data.**

How it works:
- You create a file called `.env` on your own computer
- You put YOUR API key in that file (a key you get for free from Google/Groq/etc.)
- That file **never leaves your computer** — it is blocked from upload by `.gitignore`
- Every person who downloads this app uses their **own** key with **their own** quota

### Proof It's Safe

| Check | Result |
|-------|--------|
| `.env` file in GitHub repository | ❌ Does NOT exist (blocked by .gitignore) |
| API keys in source code | ❌ None — all code reads from environment variables |
| Your key shared with others | ❌ Impossible — each user sets up their own |
| App connects to any server except AI providers | ❌ Only connects to news RSS feeds and your chosen AI API |

### What Each User Must Do

Every person who downloads this app must:
1. Get their own free API key (10 seconds, no credit card needed for free options)
2. Create their own `.env` file with their own key
3. That's it — they use their own quota, you use yours

---

## Features — What Works Without API Key vs What Needs One

### ✅ Works Immediately — No API Key Required

These features work the moment you download and run the app:

| Feature | How |
|---------|-----|
| **News collection from 74 sources** | RSS feed reading (just internet connection) |
| **Article list & viewing** | Local file reading |
| **Bookmarks & reading history** | Saved on your computer |
| **Advanced search & filters** | Local data processing |
| **Export (PDF / Markdown)** | Local file generation |
| **In-app article reader** | Web page fetch |
| **Timeline view** | Local data display |

### 🔑 Requires API Key (Free Options Available)

These features use AI — you need one free API key:

| Feature | Why API Key |
|---------|-------------|
| **AI news categorization** | AI reads and classifies each article |
| **3-line Korean summary** | AI summarizes each article |
| **Daily briefing (Top 5)** | AI selects and explains top news |
| **English → Korean translation** | AI translates article content |
| **AI news chatbot** | AI answers your questions about news |
| **Fact-check** | AI cross-verifies sources |
| **AI debate** | AI generates pros/cons for any two tools |
| **AI glossary** | AI explains technical terms |
| **Weekly intelligence report** | AI generates weekly analysis |
| **One-click full pipeline** | Runs all AI features at once |

> **The free Gemini API key** (from Google) allows 1,000 AI calls per day — more than enough for personal daily use.

---

## Highlights

- **50+ features** across 5 tabs
- **74 sources** — General AI (26) + Image & Video (20) + Vibe Coding (19) + Ontology (9)
- **35 LLM platforms** — most with free tiers, only one API key needed
- **9 categories** — Tools, Research, Trends, Tutorials, Business, Image/Video, Vibe Coding, Ontology, Other
- **19 tracked AI tools** with automatic release detection
- **5 SNS platforms** — X, Telegram, Discord, Threads, Instagram + auto card news
- **Voice briefing**, AI fact-check, AI glossary, AI debate
- **One-click full pipeline** — Collect > Analyze > Brief > Detect releases
- **Desktop app** with system tray + background notifications
- **GitHub Actions** — automated collection 3 times daily

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
| AI Fact-Check | Cross-source verification |
| Duplicate Merging | Same story from multiple outlets merged automatically |
| Keyword Watchlist | Highlight and alert on your tracked keywords |
| In-App Reader | Read full articles inside the dashboard (ad-free) |
| Advanced Search | Filter by keyword, category, sentiment, and read status |
| Bookmarks + Memo | Save articles with personal notes |
| Pagination | 10 articles per page |
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
| AI Debate | AI generates pros, cons, and verdict for any two tools |
| Weekly Intelligence Report | Deep-dive weekly analysis with predictions |

### Share Tab

| Feature | Description |
|---------|-------------|
| SNS Auto-Post | Post to X, Telegram, Discord, Threads, and Instagram |
| Card News Generator | Auto-generate 1080×1080 card images (dark theme) |
| AI Content Generation | Auto-generate tweets, threads, Instagram captions, blog posts, LinkedIn posts |
| Newsletter Email | Send formatted briefings to subscriber lists |
| Export | Download as Markdown or PDF |

### System Features

| Feature | Description |
|---------|-------------|
| One-Click Full Pipeline | Collect > AI Process > Briefing > Release Detection in one click |
| Parallel Crawling | 15 concurrent workers for fast collection |
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
| **Free (Recommended)** | Gemini ⭐, Groq ⭐, Cerebras, SambaNova, xAI, Mistral, Cohere, HuggingFace, NVIDIA, Cloudflare, Zhipu, Kluster, GLHF, Hyperbolic |
| **Credits / Budget** | Together AI, OpenRouter, Fireworks, DeepSeek, DeepInfra, Perplexity, AI21, Upstage, Lepton, Novita, Nebius, Chutes, Replicate, Alibaba, Moonshot, Yi, Baichuan |
| **Premium** | OpenAI, Azure OpenAI, Anthropic Claude, Reka AI |

> ⭐ **Recommended for beginners:** Gemini (1,000 free calls/day) and Groq (14,400 free calls/day) — no credit card needed.

---

## Getting Started — Complete Beginner Guide (Step by Step)

> **Zero coding experience needed.** If you can copy and paste text, you can set this up. Follow each step carefully.

### Step 1 — Install Python

Python is the programming language this app is built with. You need to install it once.

1. Go to: **https://www.python.org/downloads/**
2. Click the big yellow **"Download Python"** button
3. Run the downloaded file (the `.exe` file on Windows)
4. ⚠️ **VERY IMPORTANT:** At the bottom of the installer screen, check the box that says **"Add Python to PATH"**
5. Click **"Install Now"**
6. Wait for it to finish, then click "Close"

**Verify it worked:** Press `Win + R`, type `cmd`, press Enter. In the black window that appears, type:
```
python --version
```
You should see something like `Python 3.11.9`. If you do, Python is installed correctly.

---

### Step 2 — Download This Project

**Option A: Direct Download (Easiest)**
1. Go to: **https://github.com/sodam-ai/ai-news-radar**
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Find the downloaded ZIP file (usually in your Downloads folder)
5. Right-click it > **"Extract All"** > Choose a folder > Click "Extract"
6. You now have a folder called `ai-news-radar-main` (or similar)

**Option B: Git Clone (if you have Git installed)**
```bash
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

---

### Step 3 — Open a Terminal in the Project Folder

1. Open the extracted folder (the one containing `app.py`)
2. Click in the address bar at the top of File Explorer
3. Type `cmd` and press Enter
4. A black terminal window opens, already inside the correct folder ✅

---

### Step 4 — Install Required Packages

In the terminal window, type this and press Enter:
```bash
pip install -r requirements.txt
```
Wait until it finishes (1–3 minutes). You'll see many lines of text scrolling — this is normal.

---

### Step 5 — Get Your Free API Key

You need a free API key to use AI features. Here's the fastest option:

**Option A: Google Gemini (Recommended — 1,000 free calls/day)**
1. Go to: **https://aistudio.google.com/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Click **"Create API key in new project"**
5. Copy the key that appears (it looks like `AIzaSy...`)

**Option B: Groq (Also free — 14,400 free calls/day, faster)**
1. Go to: **https://console.groq.com/keys**
2. Sign up with Google (10 seconds)
3. Click **"Create API Key"**
4. Copy the key (starts with `gsk_`)

> ✅ **No credit card required** for either option. You will NOT be charged anything.

---

### Step 6 — Set Up Your API Key

1. In the project folder, find the file named **`.env.example`**
2. Copy that file and rename the copy to **`.env`** (remove the `.example` part)
   - On Windows: Right-click > Copy > Paste > Rename
3. Open `.env` with Notepad (right-click > Open with > Notepad)
4. Find the line for your chosen provider and add your key:

**If you got a Gemini key:**
```
GEMINI_API_KEY=AIzaSy_paste_your_key_here
```

**If you got a Groq key:**
```
GROQ_API_KEY=gsk_paste_your_key_here
```

5. Save and close the file

> 🔒 **Your key is safe.** This `.env` file stays on your computer only. It will never be uploaded to GitHub or shared with anyone.

---

### Step 7 — Launch the App

**Web mode (opens in your browser):**
```bash
streamlit run app.py
```
Your browser automatically opens to **http://localhost:6601**

**Desktop mode (native window):**
```bash
python desktop.py
```

**Windows shortcut:** Double-click **`AI_News_Radar.bat`** in the project folder.

---

### First Use — What to Do After Launch

1. In the sidebar (left panel), click **"📡 Collect"** — waits about 1 minute to gather news from 74 sources
2. Click **"🤖 AI Process"** — AI reads and analyzes all articles (needs API key)
3. Click **"📋 Briefing"** — generates today's Top 5 summary
4. Explore the 5 tabs: Dashboard / News Feed / AI / Insights / Share

> 💡 **Tip:** If you don't have an API key yet, you can still click "Collect" to gather news. The list will appear but without AI summaries or categories. Add your API key later to unlock AI features.

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
| Generate SNS content | Share tab > Content Generation |
| Post to social media | Share tab > SNS Posting |
| Listen to briefing | Dashboard tab > Select voice > Click "Voice" |
| Export as PDF | Share tab > Export view |
| Save an article | News Feed tab > Click bookmark icon |
| Set keyword alerts | Sidebar > Watchlist > Enter keyword |
| Run full pipeline | Sidebar > "⚡ One-Click Pipeline" button |

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
├── .env.example                 # API key template (safe to share)
├── .env                         # YOUR API keys (local only, never uploaded)
├── .gitignore                   # Blocks .env from being uploaded
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
│   ├── release_tracker.py       #   Automatic release detection
│   ├── trend.py                 #   Keyword trend analysis
│   ├── debate.py                #   AI debate mode
│   ├── smart_alert.py           #   Desktop keyword notifications
│   ├── translator.py            #   Auto Korean translation
│   ├── deduplicator.py          #   Duplicate article merging
│   └── batch_processor.py       #   Batch parallel processing
│
├── sns/                         # SNS & sharing modules
│   ├── card_generator.py        #   1080×1080 card news images
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
├── data/                        # Local data storage (never uploaded)
│   ├── preset_sources.json      #   74 curated source definitions
│   ├── articles.json            #   Collected articles
│   ├── briefings.json           #   Generated briefings
│   └── ...
│
└── .github/workflows/
    └── collect.yml              #   GitHub Actions (3× daily auto-collect)
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.11+ |
| **Dashboard** | Streamlit 1.44+ |
| **AI Engine** | 35 LLM platforms via unified model router |
| **Charts** | Plotly |
| **Voice** | edge-tts (Microsoft neural TTS) |
| **Image Generation** | Pillow |
| **Desktop** | pywebview + pystray |
| **Notifications** | plyer |
| **RSS Parsing** | feedparser (74 source feeds) |
| **Web Scraping** | BeautifulSoup4 + requests |
| **Telegram Bot** | python-telegram-bot |
| **PDF Export** | fpdf2 |
| **Scheduling** | APScheduler + GitHub Actions |
| **Data Storage** | Local JSON (zero database setup) |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `python` not found | Reinstall Python with **"Add to PATH"** checked |
| `pip` not found | Try `python -m pip install -r requirements.txt` |
| `streamlit` not found | Run `pip install streamlit` |
| "API key not set" warning | Create `.env` with your API key (see Step 6) |
| No articles appear | Click **"Collect"** first, wait 1 min, then "AI Process" |
| AI features don't work | Make sure `.env` file exists and has a valid API key |
| Categories show 0 articles | Run `python scripts/reclassify.py` |
| Port 6601 already in use | Use `streamlit run app.py --server.port 7777` |
| Slow collection | Normal — 74 sources takes ~60 seconds |

**Common API Key Mistakes:**
- Pasting the key with extra spaces → remove all spaces
- Using a key that has expired → generate a new one
- Forgetting to save the `.env` file → make sure you click Save in Notepad

---

## Roadmap

| Phase | Features | Status |
|-------|----------|:------:|
| **Phase 1** | Collection + AI Summary + Dashboard | ✅ Done |
| **Phase 2** | Search + Bookmarks + Chat + Voice + Fact-check | ✅ Done |
| **Phase 3** | Insights + SNS + Pipeline + Desktop | ✅ Done |
| **Next** | ChromaDB vector search, Ollama local LLM, Mobile PWA | 📋 Planned |

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

Copyright (c) 2026 **SoDam AI Studio**

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

---

<div align="center">

*Built with Streamlit + 35 AI Platforms by SoDam AI Studio*

</div>
