# AI News Radar

<p align="center">
  <img src="assets/icon.png" width="80" alt="AI News Radar Icon" />
</p>
<p align="center">
  <strong>パーソナルAIニュースインテリジェンスプラットフォーム</strong><br/>
  74のソースからAIニュースを自動収集・要約・分析
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-SoDam%20AI%20Studio-green"/>
  <img src="https://img.shields.io/badge/Release-v1.2.1-blue"/>
  <img src="https://img.shields.io/badge/LLM-35%20Providers-purple"/>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README_KO.md">한국어</a> |
  <a href="README_JA.md">日本語</a> |
  <a href="README_ZH.md">中文</a>
</p>

---

## クイックスタート（4ステップ）

> **プログラミング経験は不要です。**

### ステップ1：Pythonのインストール
1. **[python.org/downloads](https://www.python.org/downloads/)** にアクセス
2. **「Download Python」** をクリック
3. インストーラーを実行
4. **重要：「Add Python to PATH」にチェック！**
5. **「Install Now」** をクリック

### ステップ2：ダウンロード
[Releasesページ](https://github.com/sodam-ai/ai-news-radar/releases)から **`AI_News_Radar_v1.2.1.zip`** をダウンロード → 解凍

### ステップ3：無料APIキーの取得
1. **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)** にアクセス
2. Googleアカウントでログイン → **「Create API Key」** → キーをコピー

> **本当に無料？** はい！Googleは1日1,000回のAPI呼び出しを無料提供。個人利用に十分です。

### ステップ4：起動
**`AI_News_Radar.exe`** をダブルクリック

**初回起動時：**
- 自動で仮想環境を作成し、依存パッケージをインストールします
- **3〜5分かかります**（約200MBのダウンロード）
- テキストエディタが開いたら、APIキーを貼り付けて保存
- ブラウザにAI News Radarが表示されます！

**2回目以降：** exeをダブルクリック → 数秒で起動

---

## 主な機能（45以上）

### ニュース収集
- **74のRSSソース**から自動収集（英語＋韓国語）
- 重複ニュースの自動統合、キーワードウォッチリスト、自動翻訳

### AI分析
- 毎日TOP5ブリーフィング、週間レポート、AIチャット
- トレンド分析、リリース追跡、競合比較、ディベート、用語辞典、ファクトチェック

### コンテンツ＆共有
- 音声ブリーフィング（TTS）、Markdown/PDFエクスポート
- Discord、Telegram、X、Threads、Instagramへの投稿
- AIコンテンツ自動生成、メールニュースレター

### 対応AIプロバイダー：35サービス
Google Gemini（推奨・無料）、Groq、OpenAI、Anthropic、Mistral、Cohere など

---

## 環境変数

| 変数 | 必須 | 説明 |
|------|------|------|
| `GEMINI_API_KEY` | 推奨 | Google Gemini（無料：1,000回/日） |
| `GROQ_API_KEY` | 代替 | Groq（無料：14,400回/日） |
| `OPENAI_API_KEY` | 代替 | OpenAI GPT（有料） |

35サービスの全リストは `.env.example` を参照。

---

## トラブルシューティング

**「API key not configured」** → `.env`ファイルのAPIキーを確認

**exeをダブルクリックしても何も起きない** → Pythonが「Add to PATH」でインストールされているか確認

**初回起動が遅い** → 正常です。約200MBのパッケージをダウンロード中（3〜5分）

**Mac/Linux** → ターミナルで：
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 6601
```

---

## ライセンス

Copyright (c) 2026 **SoDam AI Studio**. All rights reserved.

本ソフトウェアは個人利用および教育目的で提供されています。
