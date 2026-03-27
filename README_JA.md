<div align="center">

# AI News Radar

**AIニュースを自動収集・分析・配信する個人用インテリジェンスプラットフォーム — 74ソース、35 LLM対応**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.44+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![LLMs](https://img.shields.io/badge/LLMプラットフォーム-35個-blueviolet)](#35個のllmプラットフォーム)
[![Sources](https://img.shields.io/badge/ニュースソース-74個-blue)](#74個のニュースソース)
[![Commits](https://img.shields.io/badge/コミット-37個-orange)](#)
[![License](https://img.shields.io/badge/ライセンス-MIT-green)](./LICENSE)

**[English](./README.md) / [Korean](./README_KO.md) / Japanese / [Chinese](./README_ZH.md)**

</div>

---

## これは何？

AIの世界は毎時間変わっています。新モデルのリリース、ツールのアップデート、論文の発表、企業の動向 — すべてが数十のサイトに散らばっています。**AI News Radar** はそのノイズを取り除きます。**74個の厳選ソース**から継続的にニュースを収集し、AIがすべての記事を要約・分類・重要度評価・ファクトチェックして、明確で実用的なブリーフィングとして届けます。

**一言で言えば：** 74サイトを自分で巡回するのをやめましょう。AIがすべて読んで、重要なことだけ教えてくれます。

---

## 主な特徴

- **50以上の機能** — 5タブ (ダッシュボード / ニュースフィード / AI / インサイト / シェア)
- **74ソース** — 一般AI(26) + 画像・動画(20) + バイブコーディング(19) + オントロジー(9)
- **35 LLMプラットフォーム** — ほとんど無料、APIキーは1つだけ必要
- **9カテゴリー** — ツール、研究、トレンド、チュートリアル、ビジネス、画像・動画、バイブコーディング、オントロジー、その他
- **19のAIツールを追跡** — リリース自動検出
- **5つのSNSプラットフォーム** — X、Telegram、Discord、Threads、Instagram + カードニュース自動生成
- **5種類のコンテンツ** — ツイート、スレッド、Instagramキャプション、ブログ投稿、LinkedIn投稿
- **音声ブリーフィング**、AIファクトチェック、AI用語集、AIディベート
- **ワンクリック全パイプライン** — 収集 > 分析 > ブリーフィング > リリース検出
- **デスクトップアプリ** — システムトレイ + バックグラウンド通知
- **GitHub Actions** — 1日3回の自動収集
- **韓国語自動翻訳** (英語 → 韓国語)

---

## 主な機能（50以上）

### ダッシュボードタブ

| 機能 | 説明 |
|------|------|
| デイリーブリーフィング | AI生成の「今日のAIニュース TOP5」（重要度ランキング付き） |
| フォーカスブリーフィング | 画像・動画 / バイブコーディング / オントロジー専用ブリーフィング |
| カテゴリークイックフィルター | 9カテゴリーのワンクリックフィルター |
| センチメントゲージ | ポジティブ/ニュートラル/ネガティブ比率のPlotlyインタラクティブチャート |
| 音声ブリーフィング | edge-ttsでブリーフィングをAI音声で聴く |
| 週間インテリジェンスレポート | トレンド・予測・分析を含む自動生成週間レポート |
| ニュースレター | SMTPで日次・週次ブリーフィングをメール送信 |

### ニュースフィードタブ

| 機能 | 説明 |
|------|------|
| 74ソース収集 | 15ワーカー並列クロールによる高速集約 |
| AIサマリー | 各記事の3行韓国語サマリー |
| 9カテゴリー分類 | AIによる自動カテゴリー分類 |
| 重要度スコア | 記事ごとの1〜5星評価 |
| センチメント分析 | ポジティブ / ニュートラル / ネガティブタグ付け |
| AIファクトチェック | クロスソース検証（「3媒体確認済み」vs「単一ソース」） |
| 重複記事マージ | 複数媒体の同一記事を自動マージ |
| キーワードウォッチリスト | 追跡キーワードのハイライト表示とアラート |
| インアップリーダー | アプリ内で全文記事を読む（広告なし） |
| 高度な検索 | キーワード・カテゴリー・センチメント・既読状態でフィルター |
| ブックマーク + メモ | 個人メモ付きで記事を保存 |
| ページネーション | 1ページ10記事のスムーズなナビゲーション |
| タイムラインビュー | 今日 / 昨日 / 今週で閲覧 |
| 韓国語自動翻訳 | 英語記事の韓国語自動翻訳 |

### AIタブ

| 機能 | 説明 |
|------|------|
| AIニュースチャット | 収集したニュースについて自然言語で質問 |
| AI用語集 | 自動抽出AIタームと初心者向けの解説 |

### インサイトタブ

| 機能 | 説明 |
|------|------|
| AIツールリリーストラッカー | 19ツールの自動リリース検出 |
| トレンドチャート | 日次言及頻度のPlotlyラインチャート |
| ホットキーワード | 前週比上昇率のキーワード |
| AIディベート | 「Midjourney vs Flux」— AI生成の長所・短所・結論 |
| 週間インテリジェンスレポート | 深掘り週間分析と予測 |

### シェアタブ

| 機能 | 説明 |
|------|------|
| SNS自動投稿 | X、Telegram、Discord、Threads、Instagramに投稿 |
| カードニュースジェネレーター | 1080×1080カード画像自動生成（ダークテーマ、カテゴリー別カラー） |
| AIコンテンツ生成 | ツイート・スレッド・Instagramキャプション・ブログ・LinkedIn自動生成 |
| ニュースレターメール | 購読者リストへのフォーマット済みブリーフィング送信 |
| エクスポート | MarkdownまたはPDFダウンロード |

### システム機能

| 機能 | 説明 |
|------|------|
| ワンクリック全パイプライン | 収集 > AI処理 > ブリーフィング > リリース検出をワンクリックで |
| 並列クロール | 15同時ワーカーによる高速収集 |
| バッチ並列処理 | 大量記事の効率的AIバッチ処理 |
| スマートキーワードアラート | 監視キーワード出現時のデスクトップ通知 |
| デスクトップアプリ | pywebviewネイティブウィンドウ + システムトレイ + バックグラウンドモード |
| GitHub Actions | 1日3回の自動収集（設定可能） |
| Telegramボット | 7コマンドでどこからでもアクセス |

---

## 74個のニュースソース

| カテゴリー | 数 | 例 |
|-----------|:--:|-----|
| **一般AI** | 26 | TechCrunch, The Verge, MIT Tech Review, Wired, ZDNET, Ben's Bites, Ars Technica |
| **画像・動画** | 20 | Stability AI, Civitai, Runway, Reddit (StableDiffusion, midjourney, flux_ai, comfyui) |
| **バイブコーディング** | 19 | Cursor, GitHub, Anthropic, Simon Willison, Reddit (vibecoding, ClaudeAI, cursor) |
| **オントロジー** | 9 | Neo4j, Stardog, W3C, Reddit (semanticweb, KnowledgeGraphs) |

---

## 35個のLLMプラットフォーム

以下のプラットフォームから**APIキー1つだけ**あれば使えます：

| ティア | プラットフォーム |
|--------|----------------|
| **無料（推奨）** | Gemini, Groq, Cerebras, SambaNova, xAI, Mistral, Cohere, HuggingFace, NVIDIA, Cloudflare, Zhipu, Kluster, GLHF, Hyperbolic |
| **クレジット/安価** | Together AI, OpenRouter, Fireworks, DeepSeek, DeepInfra, Perplexity, AI21, Upstage, Lepton, Novita, Nebius, Chutes, Replicate, Alibaba, Moonshot, Yi, Baichuan |
| **プレミアム** | OpenAI, Azure OpenAI, Anthropic Claude, Reka AI |

> **ヒント：** GeminiとGroqが無料枠が充実していて最もセットアップが簡単です。

---

## ダッシュボード構成（5タブ）

| タブ | 内容 |
|------|------|
| **ダッシュボード** | デイリーブリーフィング、フォーカスブリーフィング、カテゴリークイックフィルター、センチメントチャート、週間レポート、ニュースレター |
| **ニュースフィード** | 全ニュース、高度な検索、ブックマーク、タイムラインビュー、ページネーション |
| **AI** | ニュースチャット、AI用語集 |
| **インサイト** | リリーストラッカー、トレンドチャート、ホットキーワード、AIディベート、週間レポート |
| **シェア** | SNS投稿、AIコンテンツ生成、カードニュース、ニュースレター、エクスポート |

---

## はじめに — 7ステップ入門ガイド

> **コーディング経験ゼロでOK。** 各ステップを丁寧に進めてください。

### ステップ1 — Pythonのインストール

1. [python.org/downloads](https://www.python.org/downloads/) にアクセス
2. 大きな黄色の **"Download Python"** ボタンをクリック
3. ダウンロードしたファイルを実行
4. **必須：** インストール画面下部の **"Add Python to PATH"** チェックボックスを必ずチェック
5. **"Install Now"** をクリック

**インストール確認：** ターミナルを開き（`Win + R` → `cmd` → Enter）次を実行：

```bash
python --version
```

`Python 3.11.x` 以上が表示されれば成功です。

### ステップ2 — プロジェクトのダウンロード

**方法A：Gitを使用（推奨）**

```bash
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**方法B：直接ダウンロード**

1. [GitHubリポジトリ](https://github.com/sodam-ai/ai-news-radar) にアクセス
2. 緑色の **"Code"** ボタン → **"Download ZIP"** をクリック
3. 任意のフォルダにZIPを解凍
4. そのフォルダでターミナルを開く

### ステップ3 — 仮想環境の作成（推奨）

```bash
python -m venv venv
```

有効化：

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

ターミナルの先頭に `(venv)` が表示されれば成功です。

### ステップ4 — 依存関係のインストール

```bash
pip install -r requirements.txt
```

必要なすべてのパッケージがインストールされます。1〜2分かかることがあります。

### ステップ5 — 無料APIキーの取得

**下記から1つだけ選んでください。** 最速セットアップは **Groq** をお勧めします：

1. [console.groq.com/keys](https://console.groq.com/keys) にアクセス
2. Googleアカウントでサインアップ（10秒）
3. **"Create API Key"** をクリック
4. キーをコピー（`gsk_` で始まります）

> 他の無料オプション：[Gemini](https://aistudio.google.com/apikey), [Cerebras](https://cloud.cerebras.ai/), [SambaNova](https://cloud.sambanova.ai/)

### ステップ6 — APIキーの設定

1. プロジェクトフォルダ内の `.env.example` ファイルを見つける
2. コピーして名前を `.env` に変更
3. `.env` をメモ帳などのテキストエディタで開く
4. APIキーを貼り付け：

```env
# 1つ以上選択：
GROQ_API_KEY=gsk_実際のキーをここに貼り付け
# GEMINI_API_KEY=your_gemini_key
# OPENAI_API_KEY=sk-your_openai_key
```

5. 保存して閉じる

> **セキュリティ注意：** `.env` ファイルは `.gitignore` に含まれており、GitHubには絶対にアップロードされません。このファイルを公開しないでください。

### ステップ7 — アプリの起動

**Webモード（ブラウザで開く）：**

```bash
streamlit run app.py
```

ブラウザで **http://localhost:6601** が自動的に開きます。

**デスクトップモード（ネイティブウィンドウ）：**

```bash
python desktop.py
```

またはWindowsで **`AI_News_Radar.bat`** をダブルクリック。

### 最初の使用

1. サイドバーの **"収集"** をクリック — 74ソースからニュースを収集（約1分）
2. **"AI処理"** をクリック — AIがすべての記事を分析・要約・分類
3. **"ブリーフィング生成"** をクリック — 今日のTOP5ブリーフィング生成
4. 5つのタブを探索してすべての機能を発見してください！

---

## 使い方ガイド

| やりたいこと | 方法 |
|------------|------|
| 今日の要約を読む | ダッシュボードタブ > ブリーフィングセクション |
| カテゴリーでフィルター | ダッシュボードタブ > カテゴリークイックフィルタークリック |
| 特定のトピックを検索 | ニュースフィードタブ > 検索ビュー > キーワード入力 |
| AIにニュースを質問 | AIタブ > チャットビュー > 質問を入力 |
| AI用語を学ぶ | AIタブ > 用語集ビュー > 閲覧または検索 |
| AIツールリリースを追跡 | インサイトタブ > リリーストラッカー |
| トレンドキーワードを確認 | インサイトタブ > トレンド |
| AIディベートを実行 | インサイトタブ > AIディベート > ツール2つ選択 |
| SNSコンテンツ生成 | シェアタブ > コンテンツ生成 > 記事+プラットフォーム選択 |
| SNSに投稿 | シェアタブ > SNS投稿 > プラットフォーム選択 > 投稿 |
| ブリーフィングを聴く | ダッシュボードタブ > 音声選択 > "音声" クリック |
| PDFエクスポート | シェアタブ > エクスポートビュー |
| 記事を保存 | ニュースフィードタブ > 記事のブックマークアイコンクリック |
| キーワードアラート設定 | サイドバー > ウォッチリスト > キーワード入力 |
| 全パイプライン実行 | サイドバー > "ワンクリックパイプライン" ボタン |

---

## SNSプラットフォーム設定

| プラットフォーム | 設定時間 | 難易度 | ガイド |
|----------------|:--------:|:------:|--------|
| Discord | 30秒 | 非常に簡単 | チャンネル設定でWebhook URLを作成 |
| Telegram | 2分 | 簡単 | @BotFatherでボット作成 |
| X (Twitter) | 10分 | 中程度 | 開発者アカウント申請 |
| Threads | 10分 | 中程度 | Meta開発者ポータル |
| Instagram | 15分 | 複雑 | Instagram Graph APIセットアップ |

詳細なステップバイステップの説明はアプリ内の **シェアタブ > SNS投稿** セクションで確認できます。

---

## プロジェクト構成

```
ai-news-radar/
├── app.py                       # メインダッシュボード（5タブ）
├── desktop.py                   # デスクトップアプリ（pywebview + システムトレイ）
├── config.py                    # 設定（9カテゴリー、ポート、パス）
├── requirements.txt             # 必要パッケージ一覧
├── .env.example                 # APIキーテンプレート
├── AI_News_Radar.bat            # Windowsランチャー（Webモード）
├── AI_News_Radar_Silent.vbs     # サイレントランチャー（コンソールなし）
│
├── ai/                          # AIモジュール14個
│   ├── model_router.py          #   35 LLMプロバイダールーティング
│   ├── briefing.py              #   日次+フォーカスブリーフィング生成
│   ├── chat.py                  #   自然言語ニュースチャット
│   ├── voice_briefing.py        #   TTS音声出力（edge-tts）
│   ├── factcheck.py             #   クロスソースファクト検証
│   ├── glossary.py              #   AI用語集
│   ├── weekly_report.py         #   週間インテリジェンスレポート
│   ├── competitor.py            #   AIツールリリース監視
│   ├── release_tracker.py       #   自動リリース検出
│   ├── trend.py                 #   キーワードトレンド分析
│   ├── debate.py                #   AIディベートモード
│   ├── smart_alert.py           #   デスクトップキーワード通知
│   ├── translator.py            #   韓国語自動翻訳
│   ├── deduplicator.py          #   重複記事マージ
│   └── batch_processor.py       #   バッチ並列処理
│
├── sns/                         # SNS・シェアモジュール
│   ├── card_generator.py        #   1080×1080カードニュース画像（Pillow）
│   ├── poster.py                #   5プラットフォームSNS投稿
│   ├── content_generator.py     #   AIコンテンツ（5種類）
│   └── newsletter.py            #   メールニュースレター（SMTP）
│
├── crawler/                     # データ収集
│   ├── rss_crawler.py           #   RSSクローラー（15並列ワーカー）
│   └── scheduler.py             #   APSchedulerスケジューリング
│
├── bot/                         # Telegram連携
│   └── telegram_bot.py          #   Telegramボット（7コマンド）
│
├── reader/                      # 記事読み取り
│   └── article_reader.py        #   インアップ記事リーダー（広告なし）
│
├── export/                      # データエクスポート
│   └── exporter.py              #   Markdown + PDFエクスポート
│
├── utils/                       # 共有ユーティリティ
│   └── helpers.py               #   共通ヘルパー関数
│
├── scripts/                     # CLIツール
│   ├── collect.py               #   スタンドアロン収集スクリプト
│   └── reclassify.py            #   カテゴリー再分類ツール
│
├── data/                        # ローカルデータストレージ
│   ├── preset_sources.json      #   74ソース定義
│   ├── sources.json             #   アクティブソース設定
│   ├── articles.json            #   収集記事
│   ├── briefings.json           #   生成ブリーフィング
│   ├── weekly_reports.json      #   週間レポートアーカイブ
│   ├── release_log.json         #   ツールリリース履歴
│   ├── audio/                   #   音声ブリーフィングファイル
│   └── cards/                   #   生成カードニュース画像
│
├── .github/workflows/
│   └── collect.yml              #   GitHub Actions（1日3回自動収集）
│
└── PRD/                         #   製品設計ドキュメント
```

**8ディレクトリに24モジュール** — **37コミット** 進行中。

---

## テックスタック

| コンポーネント | 技術 |
|--------------|------|
| **言語** | Python 3.11+ |
| **ダッシュボード** | Streamlit 1.44+ |
| **AIエンジン** | 統合モデルルーター経由の35 LLMプラットフォーム |
| **チャート** | Plotly（インタラクティブトレンドチャート、センチメントゲージ） |
| **音声** | edge-tts（MicrosoftニューラルTTS） |
| **画像生成** | Pillow（ダークテーマカードニュース） |
| **デスクトップ** | pywebview + pystray（ネイティブウィンドウ + システムトレイ） |
| **通知** | plyer（クロスプラットフォームデスクトップアラート） |
| **RSSパース** | feedparser（74ソースフィード） |
| **Webスクレイピング** | BeautifulSoup4 + requests |
| **Telegramボット** | python-telegram-bot |
| **SNS API** | tweepy (X), Telegram API, Discord Webhook, Threads API, Instagram Graph API |
| **メール** | smtplib（SMTPニュースレター） |
| **PDFエクスポート** | fpdf2（韓国語フォントサポート） |
| **スケジューリング** | APScheduler（インアップ）、GitHub Actions（CI/CD） |
| **データストレージ** | ローカルJSON（データベース設定不要） |

---

## トラブルシューティング

| 問題 | 解決方法 |
|------|---------|
| `python` が見つからない | **"Add to PATH"** にチェックしてPythonを再インストール |
| `pip` が見つからない | `python -m pip install -r requirements.txt` を使用 |
| `streamlit` が見つからない | `pip install streamlit` を実行、仮想環境の有効化を確認 |
| "APIキー未設定" 警告 | `.env` ファイルにAPIキーを1つ以上入力（ステップ6参照） |
| 記事が表示されない | **"収集"** をクリックしてから **"AI処理"** を実行 |
| カテゴリーに記事が0件 | `python scripts/reclassify.py` を実行 |
| ポート6601が使用中 | `streamlit run app.py --server.port 7777` を使用 |
| macOS/LinuxでPDFエクスポート失敗 | `NanumGothic` フォントをインストール |
| デスクトップモードが起動しない | `pip install pywebview` を確認 |
| 収集が遅い | 正常 — 74ソースを15並列ワーカーで約60秒かかります |
| edge-tts音声エラー | インターネット接続を確認（edge-ttsはオンライン必要） |

---

## ロードマップ

| フェーズ | 機能 | 状態 |
|---------|------|:----:|
| **Phase 1** | 収集 + AIサマリー + ダッシュボード（17機能） | ✅ 完了 |
| **Phase 2-A** | 検索 + ブックマーク + センチメント + チャット（5機能） | ✅ 完了 |
| **Phase 2-B** | 音声 + Telegram + ファクトチェック + 用語集 + Actions（5機能） | ✅ 完了 |
| **Tier 1** | フォーカスブリーフィング + 週間レポート + リリーストラッカー（3機能） | ✅ 完了 |
| **Tier 2** | トレンドチャート + AIディベート + ホットキーワード（3機能） | ✅ 完了 |
| **S-Tier** | スマートアラート + コンテンツ生成 + ニュースレター + SNS（4機能） | ✅ 完了 |
| **UI/UX** | 5タブリデザイン + ページネーション + カテゴリークイックフィルター + プレミアムCSS | ✅ 完了 |
| **デスクトップ** | pywebview + システムトレイ + バックグラウンド通知 | ✅ 完了 |
| **パイプライン** | ワンクリック全パイプライン + 並列クロール + バッチ処理 | ✅ 完了 |
| **翻訳** | 韓国語自動翻訳 + 重複排除 | ✅ 完了 |
| **次期** | ChromaDBベクター検索、OllamaローカルLLM、ゲーミフィケーション、モバイルPWA | 📋 予定 |

---

## コントリビューション

プルリクエストを歓迎します！

1. リポジトリをフォーク
2. フィーチャーブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを開く

---

## ライセンス

MITライセンス — Copyright (c) 2026 **SoDam AI Studio**

詳細は [LICENSE](./LICENSE) をご参照ください。

---

<div align="center">

*Streamlit + 35 AIプラットフォームで構築 — SoDam AI Studio*

</div>
