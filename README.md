# AI News Radar

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-SoDam%20AI%20Studio-green)
![Release](https://img.shields.io/badge/Release-v1.0.0-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44%2B-FF4B4B?logo=streamlit&logoColor=white)

[English](README.md) | [한국어](README_KO.md) | [日本語](README_JA.md) | [中文](README_ZH.md)

---

**AI News Radar** is an AI-powered news aggregator that automatically collects, summarizes, and analyzes news from the AI industry. It pulls articles from **70+ RSS sources**, then uses **Google Gemini** to generate summaries, assign categories, rate importance, run sentiment analysis, and extract keywords -- all in one batch.

Think of it as your personal AI news analyst that never sleeps.

---

## Table of Contents

- [Screenshots](#screenshots)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
  - [Method 1 -- Web Mode (Recommended)](#method-1----web-mode-recommended)
  - [Method 2 -- Desktop App](#method-2----desktop-app)
  - [Method 3 -- Portable EXE](#method-3----portable-exe)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Build from Source](#build-from-source)
- [SNS Posting Setup](#sns-posting-setup)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

---

## Screenshots

> Screenshots will be added here. Stay tuned!

| Dashboard | Briefing | Trend Analysis |
|:---------:|:--------:|:--------------:|
| *Coming soon* | *Coming soon* | *Coming soon* |

---

## Key Features

AI News Radar ships with **45+ features** across news collection, AI analysis, and content distribution.

### News Collection and Reading

- **Auto RSS Crawling** -- Collects articles from 70+ AI news sources on a scheduled interval
- **In-App Reader View** -- Read articles directly inside the dashboard without leaving the app
- **Direct URL Access** -- Open the original article in your browser with one click
- **Timeline View** -- Browse articles by today, yesterday, or this week
- **Keyword Watchlist** -- Set keywords you care about and get them highlighted automatically
- **Auto Korean Translation** -- Translates English articles to Korean on the fly
- **Smart Deduplication** -- Removes duplicate articles across sources

### AI Analysis (Gemini-Powered)

- **Batch Processing** -- Summarizes, categorizes, scores importance, analyzes sentiment, and extracts keywords in a single API call
- **Smart Model Routing** -- Uses Gemini Flash-Lite for lightweight tasks (classification) and Gemini Flash for heavier tasks (summaries) to save cost
- **Daily Briefing** -- Auto-generates a TOP 5 briefing every day
- **Weekly Intelligence Report** -- Comprehensive weekly analysis of AI industry trends
- **AI Chat** -- Ask questions about the collected news in natural language
- **Trend Analysis** -- Tracks hot keywords and topic shifts over time
- **AI Release Tracker** -- Monitors new AI tool and model releases
- **Competitor Comparison** -- Compare AI tools side-by-side with charts
- **AI Debate Mode** -- Generates pros and cons arguments for any AI topic
- **AI Glossary** -- Automatically extracts and defines technical terms
- **Fact Check** -- Cross-references claims across multiple sources
- **Smart Alerts** -- Notifies you when important news matches your interests

### Content and Distribution

- **Voice Briefing** -- Listen to your daily briefing via text-to-speech (Edge TTS)
- **Export** -- Save articles and briefings as Markdown or PDF
- **SNS Posting** -- Publish to Discord, Telegram, X (Twitter), Threads, and Instagram
- **AI Content Generation** -- Auto-generates social media posts from news
- **Newsletter Publishing** -- Create and send email newsletters from curated articles
- **SNS Card Generator** -- Creates visual cards for social media sharing

### User Experience

- **Dark Mode** -- Easy on the eyes, day or night
- **Streamlit Dashboard** -- Clean, responsive web interface on port 6601
- **Desktop App** -- Native window via pywebview with system tray icon
- **Portable EXE** -- No installation needed, just download and run

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| Language | Python 3.11+ |
| Web Framework | Streamlit 1.44+ |
| AI / LLM | Google Gemini API (Flash + Flash-Lite) |
| News Parsing | feedparser, BeautifulSoup4 |
| Data Visualization | Plotly |
| Scheduling | APScheduler |
| Desktop | pywebview, pystray |
| Voice | edge-tts |
| SNS | python-telegram-bot, tweepy |
| Export | fpdf2 (PDF), built-in (Markdown) |
| Build | PyInstaller, Inno Setup |

---

## Quick Start

### Prerequisites

Before you begin, make sure you have:

1. **Python 3.11 or higher** installed on your computer
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, **check the box that says "Add Python to PATH"** -- this is important!
   - To verify, open a terminal and type: `python --version`

2. **A Google Gemini API key** (free tier available)
   - Go to [Google AI Studio](https://aistudio.google.com/apikey)
   - Sign in with your Google account
   - Click "Create API Key" and copy it

---

### Method 1 -- Web Mode (Recommended)

This is the easiest way to get started. It runs AI News Radar as a web page in your browser.

**Step 1: Download the project**

```bash
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**Step 2: Install dependencies**

```bash
pip install -r requirements.txt
```

> If `pip` does not work, try `pip3` or `python -m pip install -r requirements.txt`.

**Step 3: Set your API key**

Create a file named `.env` in the project root folder:

```
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with the actual key you copied from Google AI Studio.

**Step 4: Run the app**

```bash
streamlit run app.py --server.port 6601
```

Your browser will open automatically at `http://localhost:6601`. If it does not, open that URL manually.

> To stop the app, press `Ctrl + C` in the terminal.

---

### Method 2 -- Desktop App

Runs AI News Radar in its own native window (no browser needed). A system tray icon lets you minimize it.

**Step 1-3:** Follow the same steps as Web Mode above.

**Step 4: Run the desktop app**

```bash
python desktop.py
```

The app will appear in a standalone window. You can minimize it to the system tray.

---

### Method 3 -- Portable EXE

No Python installation required. Just download, extract, and run.

1. Go to the [Releases](https://github.com/sodam-ai/ai-news-radar/releases) page
2. Download the latest `.zip` file
3. Extract it to any folder
4. Create a `.env` file in the extracted folder with your `GEMINI_API_KEY`
5. Double-click `AI_News_Radar.exe`

> On first launch, Windows SmartScreen may show a warning. Click "More info" then "Run anyway" -- this is normal for unsigned applications.

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes* | -- | Your Google Gemini API key |
| `LLM_PROVIDER` | No | `gemini` | LLM provider (`gemini`, `openai`, or `groq`) |
| `OPENAI_API_KEY` | No | -- | Required only if `LLM_PROVIDER=openai` |
| `CRAWL_INTERVAL_MINUTES` | No | `60` | How often to fetch new articles (in minutes) |

*At least one AI provider API key is required.

**Example `.env` file:**

```env
GEMINI_API_KEY=AIzaSy...your_key_here
CRAWL_INTERVAL_MINUTES=30
```

For SNS posting features, see [SNS Posting Setup](#sns-posting-setup) below.

---

## Project Structure

```
ai-news-radar/
├── app.py                  # Main Streamlit dashboard
├── config.py               # Configuration and environment variables
├── desktop.py              # Desktop app (pywebview + system tray)
├── launcher.py             # EXE launcher
├── requirements.txt        # Python dependencies
├── .env                    # Your API keys (create this yourself)
│
├── ai/                     # AI modules
│   ├── batch_processor.py  #   Batch analysis (summary + category + sentiment)
│   ├── briefing.py         #   Daily TOP 5 briefing generator
│   ├── chat.py             #   AI chat about collected news
│   ├── competitor.py       #   Competitor tool comparison
│   ├── debate.py           #   AI debate mode (pros/cons)
│   ├── deduplicator.py     #   Smart article deduplication
│   ├── factcheck.py        #   Fact checking across sources
│   ├── glossary.py         #   AI term glossary extraction
│   ├── model_router.py     #   Smart model routing (Flash vs Flash-Lite)
│   ├── release_tracker.py  #   AI tool/model release tracker
│   ├── smart_alert.py      #   Interest-based notifications
│   ├── translator.py       #   Auto Korean translation
│   ├── trend.py            #   Trend analysis + hot keywords
│   ├── voice_briefing.py   #   Text-to-speech briefing (Edge TTS)
│   └── weekly_report.py    #   Weekly intelligence report
│
├── crawler/                # News collection
│   ├── rss_crawler.py      #   RSS feed parser for 70+ sources
│   └── scheduler.py        #   APScheduler-based crawl scheduling
│
├── reader/                 # Article reading
│   └── ...                 #   In-app reader view
│
├── export/                 # Export functionality
│   └── ...                 #   Markdown and PDF export
│
├── sns/                    # Social media integration
│   ├── poster.py           #   Multi-platform posting (Discord/Telegram/X/Threads)
│   ├── content_generator.py#   AI-generated social media content
│   ├── card_generator.py   #   Visual card generator for SNS
│   └── newsletter.py       #   Newsletter publishing
│
├── bot/                    # Chat bots
│   └── ...                 #   Telegram bot integration
│
├── utils/                  # Utility helpers
│   └── ...                 #   Shared utility functions
│
├── data/                   # Data storage (JSON files)
│   └── ...                 #   Crawled articles, briefings, settings
│
├── .streamlit/             # Streamlit configuration
│   └── config.toml         #   Theme and server settings
│
├── ai_news_radar.spec      # PyInstaller build spec
├── installer.iss           # Inno Setup installer script
└── build_installer.py      # Build automation script
```

---

## Build from Source

If you want to create your own EXE or installer:

### Build Portable EXE

```bash
# Install PyInstaller
pip install pyinstaller

# Build using the spec file
pyinstaller ai_news_radar.spec
```

The output will be in the `dist/` folder.

### Build Windows Installer

Requires [Inno Setup](https://jrsoftware.org/isinfo.php) to be installed.

```bash
python build_installer.py
```

The installer will be generated in the `installer_output/` folder.

---

## SNS Posting Setup

AI News Radar can auto-post curated news to multiple social platforms. Here is a brief setup guide for each:

### Discord

1. Create a webhook in your Discord server (Server Settings > Integrations > Webhooks)
2. Copy the webhook URL
3. Add to your `.env`: `DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...`

### Telegram

1. Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
2. Get your bot token and chat ID
3. Add to your `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

### X (Twitter)

1. Apply for a [developer account](https://developer.x.com/)
2. Create a project and generate API keys
3. Add to your `.env`:
   ```
   TWITTER_API_KEY=...
   TWITTER_API_SECRET=...
   TWITTER_ACCESS_TOKEN=...
   TWITTER_ACCESS_SECRET=...
   ```

### Threads / Instagram

Follow the Meta Developer documentation to set up API access and add the relevant tokens to your `.env` file.

> All SNS features are optional. The app works perfectly fine without any SNS configuration.

---

## FAQ

**Q: Is the Gemini API free?**
A: Yes, Google offers a generous free tier for the Gemini API. For most personal use, you will not need to pay. Check the [pricing page](https://ai.google.dev/pricing) for current limits.

**Q: Can I use OpenAI instead of Gemini?**
A: Yes. Set `LLM_PROVIDER=openai` and `OPENAI_API_KEY=your_key` in your `.env` file. Groq is also supported with `LLM_PROVIDER=groq`.

**Q: The app is not loading any articles. What should I do?**
A: Wait a moment after first launch -- the initial crawl takes 1-2 minutes. If articles still do not appear, check that your API key is set correctly in the `.env` file.

**Q: How do I add or remove RSS sources?**
A: RSS sources are managed in the crawler module. Edit `crawler/rss_crawler.py` to add or remove feed URLs.

**Q: Can I change the crawl frequency?**
A: Yes. Set `CRAWL_INTERVAL_MINUTES` in your `.env` file. The default is 60 minutes.

**Q: Windows shows a security warning when I run the EXE.**
A: This is normal for unsigned applications. Click "More info" then "Run anyway". The app is safe -- you can verify by reviewing the source code.

**Q: How much disk space does it use?**
A: The app itself is lightweight (under 50 MB). Collected article data grows over time but typically stays under 100 MB for weeks of usage.

**Q: Can I run this on Mac or Linux?**
A: The web mode (Streamlit) works on any OS with Python. The desktop mode (pywebview) also supports Mac and Linux. The portable EXE is Windows-only.

---

## Contributing

Contributions are welcome! Here is how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and test them
4. Commit: `git commit -m "Add my feature"`
5. Push: `git push origin feature/my-feature`
6. Open a Pull Request

Please make sure your code follows the existing style and includes appropriate comments.

---

## License

Copyright (c) 2026 **SoDam AI Studio**. All rights reserved.

This software is provided for personal and educational use. For commercial use, please contact the publisher.

See the [LICENSE](LICENSE) file for details.
