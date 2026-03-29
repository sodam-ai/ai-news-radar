# AI News Radar

<p align="center">
  <img src="assets/icon.png" width="80" alt="AI News Radar Icon" />
</p>
<p align="center">
  <strong>Your Personal AI News Intelligence Platform</strong><br/>
  Automatically collects, summarizes, and analyzes AI news from 74 sources
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/License-SoDam%20AI%20Studio-green" alt="License"/>
  <img src="https://img.shields.io/badge/Release-v1.2.1-blue" alt="Release"/>
  <img src="https://img.shields.io/badge/Streamlit-1.44%2B-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/LLM-35%20Providers-purple" alt="LLM"/>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README_KO.md">한국어</a> |
  <a href="README_JA.md">日本語</a> |
  <a href="README_ZH.md">中文</a>
</p>

---

## What is AI News Radar?

AI News Radar is a **local desktop application** that:

- Collects AI news from **74 RSS sources** (English + Korean) in one click
- Uses AI to **summarize, categorize, and analyze** every article
- Generates **daily TOP 5 briefings** and **weekly intelligence reports**
- Lets you **chat with AI** about the news ("What happened in AI today?")
- Creates **social media posts** automatically for Discord, Telegram, X, and more
- Tracks **AI tool releases**, **trends**, and **competitor movements**

Think of it as your **personal AI news assistant** that runs entirely on your computer.

---

## Quick Start Guide

> **No coding experience needed.** Just follow these steps.

### Step 1: Install Python

If Python is already installed on your computer, skip to Step 2.

1. Open your web browser and go to **[python.org/downloads](https://www.python.org/downloads/)**
2. Click the big yellow **"Download Python 3.xx"** button
3. Open the downloaded file to start the installer
4. **VERY IMPORTANT**: At the bottom of the installer, there is a checkbox that says **"Add Python to PATH"**. **You MUST check this box!** Without it, the app cannot find Python.
5. Click **"Install Now"** and wait for it to finish
6. Click **"Close"** when done

### Step 2: Download AI News Radar

**Option A — From GitHub Releases (recommended):**
1. Go to the [Releases page](https://github.com/sodam-ai/ai-news-radar/releases)
2. Download **`Source code (zip)`**
3. Right-click the ZIP file → **"Extract All"** → Choose a folder (e.g., Desktop) → **"Extract"**

**Option B — From this page:**
1. Click the green **"Code"** button at the top of this page
2. Click **"Download ZIP"**
3. Extract the ZIP to any folder

### Step 3: Get Your Free API Key

AI News Radar uses AI to analyze news. You need a free API key (takes 30 seconds):

1. Go to **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. Sign in with any Google account
3. Click **"Create API Key"**
4. **Copy the key** (it looks like `AIzaSy...`)
5. Keep this page open — you'll need to paste the key in the next step

> **Is it really free?** Yes! Google provides 1,000 free API calls per day, which is more than enough for personal news tracking. No credit card required.

### Step 4: Run the App

Open the extracted folder and **double-click `AI_News_Radar.exe`**.

**On first run:**
- The app will **automatically create a virtual environment** and **install all dependencies**
- **This takes 3-5 minutes** depending on your internet speed (about 200MB of downloads)
- A text editor will open — **paste your API key** from Step 3, save the file, and close it
- Your browser will open with AI News Radar!

**On subsequent runs:**
- Just double-click the exe again — it starts in seconds

> **Windows SmartScreen warning?** Since this is a new application, Windows may show a blue warning screen. Click **"More info"** → **"Run anyway"**. This is normal for any new software.

---

## Features Overview (45+)

### News Collection & Management
| Feature | Description |
|---------|-------------|
| One-Click Pipeline | Collect → Analyze → Briefing in a single button press |
| 74 RSS Sources | Covers TechCrunch, Ars Technica, MIT Tech Review, AI-focused blogs, Korean tech sites |
| Smart Deduplication | Same story from multiple sources? Merged automatically |
| Keyword Watchlist | Highlight articles matching your interests (e.g., "GPT", "diffusion") |
| Bookmark System | Save articles for later with instant access |
| Auto Translation | English articles translated to Korean automatically |
| Category Filters | AI Tools, Research, Trends, Tutorials, Business, Image/Video, Coding, Ontology |

### AI Analysis & Intelligence
| Feature | Description |
|---------|-------------|
| Daily TOP 5 Briefing | AI picks and summarizes the 5 most important stories |
| Weekly Report | Comprehensive analysis with trends, predictions, key takeaways |
| AI Chat | Ask questions about the news: "What are the latest LLM developments?" |
| Trend Analysis | Charts showing topic evolution over time |
| Release Tracker | Monitors new versions of 50+ AI tools |
| Competitor Analysis | Side-by-side comparison of AI companies and tools |
| AI Debate | Pro vs con analysis of controversial AI topics |
| Glossary | Technical terms explained in plain language |
| Fact Check | Cross-references claims across multiple sources |
| Smart Alerts | Notifications when news matches your interests |

### Content Creation & Sharing
| Feature | Description |
|---------|-------------|
| Voice Briefing | Listen to your daily briefing (text-to-speech, 20+ voices) |
| Export to Markdown | Clean export for blogs, Notion, Obsidian |
| Export to PDF | Formatted PDF with cover page and table of contents |
| Discord Posting | Send news and briefings to Discord channels |
| Telegram Channel | Automated posting to Telegram |
| X (Twitter) Posting | Share news on X with auto-generated captions |
| Threads / Instagram | Post to Meta platforms |
| AI Content Generator | Auto-writes social media captions optimized for each platform |
| Email Newsletter | Send weekly digests via email |

### Supported AI Providers (35)
<details>
<summary>Click to see all 35 providers</summary>

| Provider | Free Tier | Notes |
|----------|-----------|-------|
| **Google Gemini** | 1,000 calls/day | Recommended default |
| **Groq** | 14,400 calls/day | Fastest response |
| **OpenAI (GPT)** | Paid only | Most popular |
| Anthropic (Claude) | Paid only | Best reasoning |
| Mistral AI | Free tier | European provider |
| Cohere | Free tier | Good for summaries |
| Together AI | Free credits | Many open models |
| Fireworks AI | Free tier | Fast inference |
| OpenRouter | Pay per use | Aggregator |
| DeepSeek | Free tier | Chinese provider |
| Cerebras | Free trial | Ultra-fast |
| SambaNova | Free trial | Enterprise focus |
| NVIDIA NIM | Free trial | GPU-optimized |
| AI21 Labs | Free tier | Jamba model |
| HuggingFace | Free tier | Open source hub |
| ... and 20 more | Varies | See .env.example |
</details>

---

## Project Structure

```
ai-news-radar/
│
├── AI_News_Radar.exe      ← Main executable (double-click to run)
│
├── app.py                  ← Streamlit web application (main UI)
├── config.py               ← Configuration and constants
├── setup_launcher.py       ← Launcher source code
├── requirements.txt        ← Python dependency list
│
├── .env                    ← Your API keys (auto-created on first run)
├── .env.example            ← Template showing all available settings
│
├── ai/                     ← AI analysis modules (17 modules)
│   ├── batch_processor.py  ← Batch article analysis
│   ├── briefing.py         ← Daily TOP 5 briefing generator
│   ├── chat.py             ← AI chat about news
│   ├── competitor.py       ← Competitor comparison
│   ├── debate.py           ← AI debate generator
│   ├── deduplicator.py     ← Duplicate detection
│   ├── factcheck.py        ← Cross-source fact checking
│   ├── glossary.py         ← Technical term dictionary
│   ├── model_router.py     ← Multi-provider LLM routing
│   ├── release_tracker.py  ← AI tool release monitoring
│   ├── smart_alert.py      ← Interest-based alerts
│   ├── translator.py       ← Article translation
│   ├── trend.py            ← Trend analysis
│   ├── voice_briefing.py   ← Text-to-speech briefing
│   └── weekly_report.py    ← Weekly intelligence report
│
├── crawler/                ← News collection
│   ├── rss_crawler.py      ← 74-source RSS aggregator
│   └── scheduler.py        ← Automatic collection scheduler
│
├── reader/                 ← Full article reader
│   └── article_reader.py   ← Clean text extraction
│
├── export/                 ← Export modules
│   └── exporter.py         ← Markdown & PDF generation
│
├── sns/                    ← Social media integration
│   ├── card_generator.py   ← Visual card generation
│   ├── content_generator.py← AI caption writer
│   ├── newsletter.py       ← Email newsletter
│   └── poster.py           ← Multi-platform publisher
│
├── bot/                    ← Telegram bot
│   └── telegram_bot.py     ← Telegram webhook handler
│
├── utils/                  ← Utilities
│   └── helpers.py          ← JSON I/O, logging, date helpers
│
├── data/                   ← Collected data (auto-created)
│   ├── articles.json       ← All collected articles
│   ├── briefings.json      ← Generated briefings
│   ├── bookmarks.json      ← Saved bookmarks
│   └── ...                 ← Other data files
│
├── assets/                 ← App icons
│   ├── icon.ico            ← Windows icon
│   └── icon.png            ← PNG icon
│
└── .streamlit/             ← Streamlit theme configuration
    └── config.toml
```

---

## Environment Variables Reference

All settings are in the `.env` file. At minimum, you need **one** API key.

### Required (pick one)

| Variable | Provider | Free Tier | How to Get |
|----------|----------|-----------|-----------|
| `GEMINI_API_KEY` | Google Gemini | 1,000 calls/day | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| `GROQ_API_KEY` | Groq | 14,400 calls/day | [console.groq.com](https://console.groq.com) |
| `OPENAI_API_KEY` | OpenAI | Paid ($0.002/call) | [platform.openai.com](https://platform.openai.com) |

### Optional — Social Media Posting

| Variable(s) | Platform | Setup Difficulty |
|-------------|----------|-----------------|
| `DISCORD_WEBHOOK_URL` | Discord | Easy (30 seconds) |
| `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHANNEL_ID` | Telegram | Medium (5 minutes) |
| `X_API_KEY` + `X_API_SECRET` + `X_ACCESS_TOKEN` + `X_ACCESS_SECRET` | X (Twitter) | Hard (requires developer account) |
| `THREADS_ACCESS_TOKEN` | Threads | Medium |
| `INSTAGRAM_ACCESS_TOKEN` + `INSTAGRAM_BUSINESS_ACCOUNT_ID` | Instagram | Hard |

### Optional — Email Newsletter

| Variable | Description |
|----------|-------------|
| `SMTP_SERVER` | Email server (e.g., `smtp.gmail.com`) |
| `SMTP_PORT` | Port (e.g., `587`) |
| `SMTP_USER` | Your email address |
| `SMTP_PASSWORD` | App password (not your regular password) |
| `NEWSLETTER_RECIPIENTS` | Comma-separated email list |

See `.env.example` for the complete list of all 35+ provider keys.

---

## Advanced Usage

### Run from Command Line

For users comfortable with terminals:

```bash
# Clone
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar

# Setup
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install (takes 3-5 minutes)
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your API key

# Run
streamlit run app.py --server.port 6601
```

### Run as Desktop App (with window frame)

```bash
# Install extra dependencies
pip install pywebview pystray plyer

# Run
python launcher.py
```

### Build the Launcher EXE Yourself

```bash
pip install pyinstaller
pyinstaller --onefile --name "AI_News_Radar" --icon "assets/icon.ico" --console setup_launcher.py
```

---

## Troubleshooting

### "API key not configured"
Open the `.env` file in any text editor (Notepad, VS Code, etc.) and make sure your API key is entered correctly. The format should be:
```
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxx
```
No quotes, no spaces around the `=` sign.

### Nothing happens when I double-click the exe
1. Make sure Python is installed: open Command Prompt and type `python --version`
2. If you see "not recognized", reinstall Python with **"Add to PATH"** checked
3. Try right-click → **"Run as administrator"**

### "Port 6601 already in use"
Another instance might be running. Either:
- Close the other instance (check your taskbar for the console window)
- Or the app will automatically find a different available port

### The app is slow on first run
That's normal! On the first run, it downloads and installs ~200MB of Python packages. After that, it starts in seconds.

### Windows Defender / SmartScreen blocks the exe
This happens because the exe is new and not digitally signed. Click **"More info"** → **"Run anyway"**. The exe is safe — you can verify by reading the source code in `setup_launcher.py`.

### Can I use this on Mac or Linux?
Yes! The `.exe` file is Windows-only, but the core app works on any OS. Use the command line instructions in the "Advanced Usage" section.

---

## Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| Language | Python 3.11+ | Core runtime |
| Web UI | Streamlit 1.44+ | Interactive dashboard |
| AI | 35 LLM providers | News analysis, summaries |
| News Feed | feedparser | RSS parsing |
| Web Scraping | BeautifulSoup4, requests | Full article extraction |
| Charts | Plotly | Interactive visualizations |
| Voice | edge-tts | Text-to-speech (20+ voices) |
| PDF | fpdf2 | PDF export |
| Social Media | tweepy, requests, webhooks | Multi-platform posting |
| Scheduling | APScheduler | Automatic collection |
| Desktop | pywebview (optional) | Native window mode |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test: `streamlit run app.py`
5. Commit and push
6. Open a Pull Request

---

## License

Copyright (c) 2026 **SoDam AI Studio**. All rights reserved.

This software is provided for personal and educational use.
For commercial use, please contact the publisher.

See the [LICENSE](LICENSE) file for details.
