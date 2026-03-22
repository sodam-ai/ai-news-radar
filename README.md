# AI News Radar

> **Your personal AI news dashboard that automatically collects, summarizes, and categorizes AI news.**

**Language / [Korean](./README_KO.md) / [Japanese](./README_JA.md) / [Chinese](./README_ZH.md)**

---

## What is AI News Radar?

AI News Radar is a **personal dashboard** that automatically gathers AI-related news from around the world, then uses Google's Gemini AI to summarize, categorize, and rank them by importance.

**In simple terms:** Instead of visiting 15+ news sites every day, this app does it for you and shows you only what matters.

### What It Does

| Feature | Description |
|---------|-------------|
| Auto-Collect | Automatically gathers news from 15 pre-set sources (TechCrunch, The Verge, MIT Tech Review, etc.) |
| AI Summary | Summarizes each article into 3 lines in Korean |
| Smart Categorization | Sorts news into categories: Tools, Research, Trends, Tutorials, Business |
| Importance Score | Rates each article from 1 to 5 stars |
| Sentiment Analysis | Tags each article as Positive / Neutral / Negative |
| Daily Briefing | Generates a "Top 5 AI News Today" briefing every day |
| Duplicate Merging | When multiple outlets cover the same story, merges them into one |
| Keyword Watchlist | Highlights news containing your tracked keywords (e.g., "Claude", "GPT") |
| In-App Reader | Read full articles inside the dashboard without ads |
| Dark Mode | Switch between dark and light themes |
| Export | Download briefings and articles as Markdown or PDF |
| Image Analysis | AI analyzes charts and infographics found in news articles |
| Live Updates | Dashboard refreshes automatically every 5 minutes |
| Timeline View | Browse news chronologically (Today / Yesterday / This Week) |

---

## Screenshots

After running the app, open your browser to `http://localhost:6601` to see:

- **Briefing Tab** - Today's Top 5 AI news at a glance
- **News List Tab** - All collected articles with filters
- **Timeline Tab** - Time-based news flow
- **Sources Tab** - Manage your news sources

---

## Getting Started (Step-by-Step for Beginners)

> **You don't need any coding experience.** Just follow each step carefully.

### Step 1: Install Python

Python is the programming language this app runs on. You need to install it first.

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow **"Download Python 3.xx"** button
3. Run the downloaded file
4. **IMPORTANT:** Check the box that says **"Add Python to PATH"** at the bottom of the installer
5. Click **"Install Now"**

**How to verify:** Open Command Prompt (press `Win + R`, type `cmd`, press Enter) and type:
```
python --version
```
If you see something like `Python 3.13.x`, you're good!

### Step 2: Download This Project

**Option A: Using Git (Recommended)**

If you have Git installed:
```
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**Option B: Direct Download**

1. Go to the [GitHub repository page](https://github.com/sodam-ai/ai-news-radar)
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Extract the ZIP file to any folder you like

### Step 3: Install Required Packages

Open Command Prompt, navigate to the project folder, and run:
```
cd path\to\ai-news-radar
pip install -r requirements.txt
```

> **What does this do?** It downloads all the libraries (tools) that the app needs to run.

### Step 4: Get a Gemini API Key (Free)

The AI features require a Google Gemini API key. It's **completely free**.

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated key (it looks like `AIzaSy...`)

### Step 5: Set Up Your API Key

1. In the project folder, find the file named `.env.example`
2. Make a copy of it and rename the copy to `.env`
3. Open `.env` with any text editor (Notepad is fine)
4. Replace `your_gemini_api_key_here` with your actual API key:

```
GEMINI_API_KEY=AIzaSyYourActualKeyHere
```

5. Save the file

> **Security Note:** The `.env` file contains your secret API key. It is automatically excluded from uploads to GitHub. Never share this file with anyone.

### Step 6: Run the App

```
streamlit run app.py
```

Your browser will automatically open to **http://localhost:6601**

That's it! You're now running AI News Radar!

---

## How to Use

### First Time

1. Click **"Collect"** button in the sidebar to gather news
2. Click **"AI Process"** button to analyze the collected articles
3. Click **"Generate Briefing"** to create today's Top 5 summary

### Daily Use

The app automatically collects news every 60 minutes. Just open the dashboard and check:

- **Briefing Tab** for a quick overview
- **News List** for detailed reading
- Use **filters** in the sidebar to focus on specific categories or sentiments

### Features Guide

| Action | How To |
|--------|--------|
| Add a news source | Sidebar > Source Management > Enter name and RSS URL > Click "Add Source" |
| Track a keyword | Sidebar > Keyword Watchlist > Enter keyword > Click "Add" |
| Read full article | Click article title (opens in new tab) or "Read More" > "Fetch Original" |
| Export as PDF | Briefing tab or News tab > Click "Export" > Select PDF |
| Switch dark/light mode | Sidebar > Toggle at the top |

---

## Project Structure

```
ai-news-radar/
├── app.py                  # Main dashboard (what you see in the browser)
├── config.py               # Settings (API keys, intervals)
├── requirements.txt        # List of required packages
├── .env.example            # Template for your API key
├── .env                    # Your actual API key (NOT uploaded to GitHub)
├── .streamlit/
│   └── config.toml         # Theme and port settings
├── crawler/                # News collection
│   ├── rss_crawler.py      # Fetches articles from RSS feeds
│   └── scheduler.py        # Runs collection on schedule
├── ai/                     # AI processing
│   ├── model_router.py     # Smart routing: Flash-Lite for simple, Flash for complex
│   ├── batch_processor.py  # Processes 5 articles at once + image analysis
│   ├── deduplicator.py     # Merges duplicate news
│   └── briefing.py         # Generates daily Top 5 briefing
├── reader/
│   └── article_reader.py   # Clean article reader (no ads)
├── export/
│   └── exporter.py         # Markdown and PDF export
├── data/
│   └── preset_sources.json # 15 pre-configured news sources
├── utils/
│   └── helpers.py          # Utility functions
└── PRD/                    # Design documents
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `pip` command not found | Reinstall Python and check "Add Python to PATH" |
| `streamlit` command not found | Run: `pip install streamlit` |
| "GEMINI_API_KEY not set" warning | Make sure you created `.env` file (not `.env.example`) with your key |
| No articles appear | Click "Collect" first, then "AI Process" |
| Port 6601 already in use | Close other Streamlit instances or change port in `.streamlit/config.toml` |
| PDF export fails | Make sure you're on Windows (uses Windows fonts) |

---

## Free API Limits

AI News Radar is designed to run **completely free** using Gemini's free tier:

| Model | Free Limit | Used For |
|-------|-----------|----------|
| Gemini Flash-Lite | 1,000 requests/day | Categorization, tags, sentiment |
| Gemini Flash | 250 requests/day | Summaries, briefings, image analysis |

The smart routing system automatically uses the cheaper model for simple tasks and the better model for complex tasks, maximizing what you can do for free.

---

## Roadmap

| Phase | Features | Status |
|-------|----------|--------|
| Phase 1 (MVP) | Collection + AI Summary + Dashboard (17 features) | Complete |
| Phase 2 | Chat + Voice + Bots + Fact-check + Gamification (35 features) | Planned |
| Phase 3 | Agents + Prediction + Podcast + Plugins + Team mode (19 features) | Planned |

See [PRD/03_PHASES.md](./PRD/03_PHASES.md) for the full roadmap.

---

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Language | Python 3.11+ | Best ecosystem for AI and web scraping |
| Dashboard | Streamlit 2026 | Build web UI with Python only |
| AI | Google Gemini (Flash + Flash-Lite) | Free tier, smart routing |
| Data | Local JSON files | No database server needed |
| Scheduling | APScheduler | Background collection without cron |

---

## License

This is a personal project. All rights reserved.

---

## Contributing

This project is currently for personal use. If you're interested in contributing, please open an issue first.

---

*Built with Streamlit + Google Gemini AI*
