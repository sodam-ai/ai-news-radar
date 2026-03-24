# AI News Radar

> **Your personal AI news dashboard — auto-collects, summarizes, and categorizes AI news from 74 sources with 35 LLM support.**

**Language / [Korean](./README_KO.md) / [Japanese](./README_JA.md) / [Chinese](./README_ZH.md)**

---

## What is This?

AI News Radar gathers AI-related news from around the world, then uses AI to summarize, categorize, and rank them by importance. It supports **35 LLM platforms** (most with free tiers), runs as both a **web app** and a **desktop app**, and can auto-post to **5 SNS platforms**.

**In simple terms:** Instead of visiting dozens of AI news sites every day, this app does it for you and shows you only what matters.

---

## Key Features (45+)

### Dashboard
| Feature | Description |
|---------|-------------|
| Daily Briefing | AI generates "Top 5 AI News Today" every day |
| Focus Briefing | Separate briefing for Image/Video, Vibe Coding, Ontology |
| Category Filter | Filter dashboard by 9 categories (click to see only that category) |
| Sentiment Gauge | Plotly charts showing positive/neutral/negative ratio |
| Voice Briefing | Listen to the briefing as AI-generated Korean speech |
| Weekly Report | Auto-generated weekly intelligence report with trends & predictions |
| Newsletter | Send daily/weekly briefing via email (SMTP) |

### News Feed
| Feature | Description |
|---------|-------------|
| 74 Sources | Auto-collect from 74 RSS sources worldwide |
| AI Summary | 3-line Korean summary for each article |
| 9 Categories | Tools, Research, Trends, Tutorials, Business, **Image/Video**, **Vibe Coding**, **Ontology**, Other |
| Importance Score | 1-5 stars per article |
| Sentiment Analysis | Positive / Neutral / Negative tagging |
| Fact-Check Badge | Cross-source verification ("3 outlets confirmed" vs "single source") |
| Duplicate Merging | Same story from multiple outlets merged into one |
| Keyword Watchlist | Highlight news with your tracked keywords |
| In-App Reader | Read articles inside the dashboard (no ads) |
| Search | Keyword + category + sentiment + read status filters |
| Bookmarks + Memo | Save articles with personal notes |
| Pagination | 10 articles per page with navigation |
| Timeline View | Browse by Today / Yesterday / This Week |

### AI Features
| Feature | Description |
|---------|-------------|
| AI Chat | Ask questions about collected news in natural language |
| AI Glossary | Auto-extract AI terms with beginner-friendly explanations |
| AI Debate | "Midjourney vs Flux" — AI generates pros/cons/verdict |
| AI Content | Auto-generate tweets, threads, Instagram captions, blog posts, LinkedIn posts |
| Smart Alert | Desktop notification when watched keywords are detected |
| Competitor Monitor | Track 21 AI tools across 3 categories with charts |
| Trend Charts | Daily mention frequency with interactive Plotly line charts |
| Hot Keywords | Rising keywords with week-over-week change rate |

### Sharing & Export
| Feature | Description |
|---------|-------------|
| SNS Auto-Post | Post card news to X, Telegram, Discord, Threads, Instagram |
| Card News | Auto-generate 1080x1080 card images (dark theme, per-category colors) |
| Export | Download as Markdown or PDF |
| Desktop App | Native window (pywebview) + system tray + background notifications |

---

## 74 News Sources

| Category | Count | Examples |
|----------|-------|---------|
| General AI | 26 | TechCrunch, The Verge, MIT Tech Review, Wired, ZDNET, Ben's Bites |
| Image/Video | 20 | Stability AI, Civitai, Runway, Reddit (StableDiffusion, midjourney, flux_ai, comfyui) |
| Vibe Coding | 19 | Cursor, GitHub, Anthropic, Simon Willison, Reddit (vibecoding, ClaudeAI, cursor) |
| Ontology | 9 | Neo4j, Stardog, W3C, Reddit (semanticweb, KnowledgeGraphs) |

---

## 35 LLM Platforms

You only need **one API key** from any platform:

| Tier | Platforms |
|------|-----------|
| **Free (Recommended)** | Gemini, Groq, Cerebras, SambaNova, xAI, Mistral, Cohere, HuggingFace, NVIDIA, Cloudflare, Zhipu, Kluster, GLHF, Hyperbolic |
| **Credits / Cheap** | Together AI, OpenRouter, Fireworks, DeepSeek, DeepInfra, Perplexity, AI21, Upstage, Lepton, Novita, Nebius, Chutes, Replicate, Alibaba, Moonshot, Yi, Baichuan |
| **Premium** | OpenAI, Azure OpenAI, Anthropic Claude, Reka AI |

---

## Dashboard (5 Tabs)

| Tab | What's Inside |
|-----|---------------|
| **Dashboard** | Briefing + Focus areas + Category filter + Sentiment charts + Weekly report + Newsletter |
| **News Feed** | All news / Search / Bookmarks / Timeline (switch with radio buttons) |
| **AI** | News chat / AI glossary |
| **Insights** | Tool comparison / Trends / AI Debate / Weekly report |
| **Share** | SNS posting / AI content generation / Export |

---

## Getting Started (Complete Beginner Guide)

> **Zero coding experience needed.** Follow each step carefully.

### Step 1: Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow **"Download Python"** button
3. Run the downloaded file
4. **IMPORTANT:** Check **"Add Python to PATH"** at the bottom
5. Click **"Install Now"**

**Verify:** Open Command Prompt (`Win + R` > type `cmd` > Enter) and type:
```
python --version
```
You should see something like `Python 3.13.x`.

### Step 2: Download This Project

**Option A: Using Git (Recommended)**
```
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**Option B: Direct Download**
1. Go to the [GitHub page](https://github.com/sodam-ai/ai-news-radar)
2. Click green **"Code"** button > **"Download ZIP"**
3. Extract the ZIP file
4. Open the extracted folder

### Step 3: Install Required Packages

Open Command Prompt in the project folder and run:
```
pip install -r requirements.txt
```
This installs all 14 packages automatically. Wait until it finishes.

### Step 4: Get a Free API Key

Choose **any one** platform. **Groq is the easiest:**

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up with Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `gsk_`)

### Step 5: Set Up Your API Key

1. Find the file `.env.example` in the project folder
2. Copy it and rename the copy to `.env`
3. Open `.env` with Notepad
4. Replace the example with your actual key:
```
GROQ_API_KEY=gsk_YourActualKeyHere
```
5. Save and close

> **Security:** The `.env` file is automatically hidden from GitHub. Never share this file.

### Step 6: Run the App

**Web mode (browser):**
```
streamlit run app.py
```
Browser opens to **http://localhost:6601**

**Desktop mode (native window):**
```
python desktop.py
```
Or just double-click `AI_News_Radar.bat`

### Step 7: First Use

1. Click **"Collect"** in sidebar > gathers news from 74 sources
2. Click **"AI Process"** > AI analyzes all articles
3. Click **"Generate Briefing"** > creates today's Top 5
4. Explore the dashboard!

---

## How to Use

| What You Want | How |
|---------------|-----|
| Read today's summary | Dashboard tab > Briefing section |
| See only Image/Video news | Dashboard tab > Click "AI 이미지/영상" category |
| Search for specific topic | News Feed tab > Search view > Type keyword |
| Ask AI about news | AI tab > Chat view > Type question |
| Compare AI tools | Insights tab > Tool Comparison |
| See trending keywords | Insights tab > Trends |
| Generate SNS content | Share tab > Content Generation > Select article + platform |
| Post to SNS | Share tab > SNS Posting > Select platforms > Post |
| Listen to briefing | Dashboard tab > Select voice > Click "Voice" |
| Export as PDF | Share tab > Export view |
| Save important article | News Feed tab > Click ☆ on article |
| Track a keyword | Sidebar > Watchlist > Enter keyword |

---

## SNS Setup (Quick Guide)

| Platform | Time | Difficulty |
|----------|------|-----------|
| Discord | 30 sec | Very Easy |
| Telegram | 2 min | Easy |
| X (Twitter) | 10 min | Medium |
| Threads | 10 min | Medium |
| Instagram | 15 min | Complex |

See the **Share tab > SNS Posting** section for detailed step-by-step setup guides.

---

## Project Structure

```
ai-news-radar/
├── app.py                    # Main dashboard (5 tabs, ~1000 lines)
├── desktop.py                # Desktop app (pywebview + tray)
├── config.py                 # Settings (9 categories, 3 sentiments)
├── requirements.txt          # 14 packages
├── ai/                       # 14 AI modules
│   ├── model_router.py       #   35 LLM providers
│   ├── briefing.py           #   Daily + focus briefing
│   ├── chat.py               #   AI news chat
│   ├── voice_briefing.py     #   TTS voice (edge-tts)
│   ├── factcheck.py          #   Cross-source verification
│   ├── glossary.py           #   AI term dictionary
│   ├── weekly_report.py      #   Weekly intelligence report
│   ├── competitor.py         #   21 tool monitoring
│   ├── trend.py              #   Keyword trend analysis
│   ├── debate.py             #   AI debate mode
│   └── smart_alert.py        #   Desktop notifications
├── sns/                      # SNS modules
│   ├── card_generator.py     #   Card news image (Pillow)
│   ├── poster.py             #   5 platform adapters
│   ├── content_generator.py  #   AI content (5 types)
│   └── newsletter.py         #   Email newsletter (SMTP)
├── bot/telegram_bot.py       # Telegram bot (7 commands)
├── scripts/                  # CLI tools
│   ├── collect.py            #   Auto-collect script
│   └── reclassify.py         #   Category reclassifier
├── .github/workflows/        # GitHub Actions (3x daily)
├── crawler/                  # RSS collection
├── reader/                   # Ad-free article reader
├── export/                   # Markdown + PDF export
├── data/                     # 74 preset sources
└── PRD/                      # Design documents
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `pip` not found | Reinstall Python with "Add to PATH" checked |
| `streamlit` not found | Run: `pip install streamlit` |
| "API key not set" warning | Create `.env` file with at least one API key |
| No articles appear | Click "Collect" first, then "AI Process" |
| Category filter shows 0 | Run: `python scripts/reclassify.py` to reclassify existing articles |
| Port in use | Use `streamlit run app.py --server.port 7429` |
| PDF export fails | Windows only (uses Korean fonts) |

---

## Roadmap

| Phase | Features | Status |
|-------|----------|--------|
| Phase 1 | Collection + AI Summary + Dashboard (17) | **Complete** |
| Phase 2-A | Search + Bookmarks + Sentiment + Chat (5) | **Complete** |
| Phase 2-B | Voice + Telegram + Fact-check + Glossary + Actions (5) | **Complete** |
| Tier 1 | Focus Briefing + Weekly Report + Competitor Monitor (3) | **Complete** |
| Tier 2 | Trend Charts + AI Debate (2) | **Complete** |
| S-Tier | Smart Alert + Content Gen + Newsletter + SNS (4) | **Complete** |
| UI/UX | 5-tab redesign + Pagination + Premium CSS | **Complete** |
| Desktop | pywebview + System Tray + Notifications | **Complete** |
| Next | Auto-translation, ChromaDB, Ollama, Gamification | Planned |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| Dashboard | Streamlit |
| AI | 35 LLM platforms |
| Charts | Plotly |
| Voice | edge-tts (Microsoft TTS) |
| Images | Pillow (card news) |
| Desktop | pywebview + pystray |
| Bot | python-telegram-bot |
| SNS | tweepy (X), Telegram API, Discord Webhook, Threads API, Instagram Graph API |
| CI/CD | GitHub Actions |
| Data | Local JSON |

---

## License

MIT License - Copyright (c) 2026 **SoDam AI Studio**

See [LICENSE](./LICENSE) for details.

---

*Built with Streamlit + 35 AI Platforms by SoDam AI Studio*
