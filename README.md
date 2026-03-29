# AI News Radar

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-SoDam%20AI%20Studio-green)
![Release](https://img.shields.io/badge/Release-v1.1.0-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44%2B-FF4B4B?logo=streamlit&logoColor=white)

[English](README.md) | [한국어](README_KO.md) | [日本語](README_JA.md) | [中文](README_ZH.md)

---

**AI News Radar** collects AI news from **74 sources**, then uses AI to summarize, categorize, and analyze everything automatically. Think of it as your personal AI news assistant.

---

## How to Run (3 Steps)

> **You do NOT need any coding experience.** Just follow these 3 steps.

### Step 1: Download

Click the green **"Code"** button at the top of this page, then click **"Download ZIP"**.

Extract (unzip) the downloaded file to any folder on your computer.

### Step 2: Install Python

If you already have Python installed, skip this step.

1. Go to **[python.org/downloads](https://www.python.org/downloads/)**
2. Click the big yellow **"Download Python"** button
3. Run the downloaded file
4. **IMPORTANT: Check the box at the bottom that says "Add Python to PATH"**
5. Click **"Install Now"**

### Step 3: Run the App

Open the folder where you extracted the files, and **double-click** one of these files:

| File | What it does |
|------|-------------|
| **`install_and_run.bat`** | **Use this the first time.** It installs everything and helps you set up your API key. |
| **`start.bat`** | **Use this after the first time.** Quick launch. |

That's it! Your browser will open with AI News Radar.

---

## Getting Your Free API Key

AI News Radar needs an AI service to analyze news. The recommended free option is **Google Gemini**.

1. Go to **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key

The `install_and_run.bat` script will ask you to paste this key automatically.

> **35 AI services are supported.** See the `.env.example` file for the full list. You only need ONE key.

---

## Features (45+)

### News Collection
- Auto-collects from **74 RSS sources** (English + Korean)
- Smart deduplication across sources
- Keyword watchlist with highlighting
- Auto Korean translation

### AI Analysis
- **One-click pipeline**: Collect → Analyze → Briefing in one button
- Daily TOP 5 briefing
- Weekly intelligence report
- AI chat (ask questions about the news)
- Trend analysis with charts
- AI tool release tracker
- Competitor comparison
- AI debate mode (pros vs cons)
- AI glossary (explains technical terms)
- Fact checking across sources
- Smart alerts for your interests

### Content & Sharing
- Voice briefing (text-to-speech)
- Export to Markdown / PDF
- Post to Discord, Telegram, X, Threads, Instagram
- AI content generator (auto-writes social posts)
- Newsletter publishing via email

---

## Project Structure

```
ai-news-radar/
├── install_and_run.bat    ← Double-click to set up & run (first time)
├── start.bat              ← Double-click to run (after first time)
├── desktop.bat            ← Run as desktop app (optional)
├── app.py                 ← Main application
├── config.py              ← Settings
├── requirements.txt       ← Dependencies list
├── .env                   ← Your API keys (you create this)
├── .env.example           ← Template for .env
│
├── ai/                    ← AI analysis modules
├── crawler/               ← News collection
├── reader/                ← Article reader
├── export/                ← Markdown/PDF export
├── sns/                   ← Social media posting
├── bot/                   ← Telegram bot
├── utils/                 ← Utility functions
├── data/                  ← Collected news data (auto-created)
└── assets/                ← App icon
```

---

## Environment Variables

All settings are stored in the `.env` file. At minimum, you need ONE API key.

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Recommended | Google Gemini (free: 1000 calls/day) |
| `GROQ_API_KEY` | Alternative | Groq (free: 14,400 calls/day) |
| `OPENAI_API_KEY` | Alternative | OpenAI GPT (paid) |

See `.env.example` for all 35 supported AI services.

**For SNS posting** (optional):

| Variable | Platform |
|----------|----------|
| `DISCORD_WEBHOOK_URL` | Discord (easiest, 30 seconds to set up) |
| `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHANNEL_ID` | Telegram |
| `X_API_KEY` + `X_API_SECRET` + `X_ACCESS_TOKEN` + `X_ACCESS_SECRET` | X (Twitter) |

---

## Advanced: Run from Terminal

If you prefer using the command line:

```bash
# Clone the repository
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar

# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit .env
cp .env.example .env
# Edit .env and add your API key

# Run
streamlit run app.py --server.port 6601
```

---

## FAQ

**Q: The app shows "API key not configured"**
A: Open the `.env` file in Notepad and make sure your API key is entered correctly. No quotes needed.

**Q: Nothing happens when I double-click the .bat file**
A: Right-click the .bat file → "Run as administrator". If that doesn't work, make sure Python is installed with "Add to PATH" checked.

**Q: Can I use this on Mac or Linux?**
A: Yes! Use the terminal commands in the "Advanced" section above. The `.bat` files are Windows-only.

**Q: Is the Gemini API really free?**
A: Yes. Google offers 1000 calls/day for Flash-Lite and 250 calls/day for Flash, free of charge. More than enough for personal use.

**Q: How do I update to a new version?**
A: Download the new ZIP, extract it to the same folder, and run `start.bat`. Your `.env` file and `data/` folder will be preserved.

---

## Tech Stack

| Category | Technology |
|----------|-----------|
| Language | Python 3.11+ |
| Web UI | Streamlit |
| AI | 35 LLM providers (Gemini recommended) |
| News | feedparser, BeautifulSoup4 |
| Charts | Plotly |
| Voice | edge-tts |
| SNS | Telegram, Discord, X, Threads, Instagram |
| Export | Markdown, PDF (fpdf2) |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes
4. Push and open a Pull Request

---

## License

Copyright (c) 2026 **SoDam AI Studio**. All rights reserved.

This software is provided for personal and educational use.
For commercial use, please contact the publisher.

See the [LICENSE](LICENSE) file for details.
