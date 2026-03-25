# AI News Radar

> **AIニュースを自動収集・要約・分類する個人用ダッシュボード — 74ソース、35 LLM、50以上の機能**

**[English](./README.md) / [Korean](./README_KO.md) / Japanese / [Chinese](./README_ZH.md)**

---

## これは何？

AI News Radarは、世界中のAIニュースを**自動収集**し、AIが**要約・分類・重要度評価**を行う個人用ダッシュボードです。**35のLLMプラットフォーム**対応（ほとんど無料）、**Web＋デスクトップ**両対応、**5つのSNS**への自動投稿も可能です。

**一言で言えば：** 毎日数十のAIニュースサイトを巡回する代わりに、このアプリが代行して重要なものだけを表示します。

---

## ダッシュボード（5タブ）

| タブ | 内容 |
|------|------|
| **Dashboard** | ブリーフィング + 関心分野 + カテゴリフィルター + 感情チャート + 週間レポート + ニュースレター |
| **News Feed** | 全ニュース / 検索 / ブックマーク / タイムライン |
| **AI** | ニュースチャット / AI用語辞典 |
| **Insights** | ツール比較 / トレンド / AIディベート / 週間レポート |
| **Share** | SNS投稿 / AIコンテンツ生成 / エクスポート |

---

## 主な機能（50以上）

### ダッシュボード
| 機能 | 説明 |
|------|------|
| デイリーブリーフィング | AIが毎日「今日のAIニュース TOP 5」を自動生成 |
| 関心分野ブリーフィング | 画像/動画、バイブコーディング、オントロジー分野別カスタムブリーフィング |
| カテゴリフィルター | 9カテゴリでワンクリックフィルター（件数表示） |
| 感情チャート | ポジティブ/ニュートラル/ネガティブ比率のPlotlyチャート |
| 音声ブリーフィング | ブリーフィングをAI音声で聴く（女性/男性選択） |
| 週間レポート | トレンド＋分野別動向＋予測の自動生成レポート |
| ニュースレター | 日次/週次ブリーフィングをメール自動送信（SMTP） |

### ニュースフィード
| 機能 | 説明 |
|------|------|
| 74ソース自動収集 | 全世界74のRSSソースから並列クローリングで自動収集 |
| AI要約 | 各記事を3行で要約 |
| 9カテゴリ | ツール、研究、トレンド、チュートリアル、ビジネス、**画像/動画**、**バイブコーディング**、**オントロジー**、その他 |
| 重要度スコア | 各記事に1〜5つ星 |
| 感情分析 | ポジティブ / ニュートラル / ネガティブ タグ |
| ファクトチェック | 複数ソース照合（「3媒体確認」vs「単独報道」） |
| 重複統合 | 同一ニュースを自動マージ |
| キーワードウォッチリスト | 追跡キーワードを含むニュースをハイライト |
| アプリ内リーダー | ダッシュボード内で記事を閲覧（広告なし） |
| 検索 | キーワード＋カテゴリ＋感情＋既読状態フィルター |
| ブックマーク＋メモ | 記事保存＋個人メモ |
| ページネーション | 10件ずつページ送り |
| タイムラインビュー | 今日 / 昨日 / 今週で閲覧 |

### AI機能
| 機能 | 説明 |
|------|------|
| AIチャット | 収集ニュースについて自然言語で質問 |
| AI用語辞典 | 専門用語を初心者にも分かりやすく自動解説 |
| AIディベート | 「Midjourney vs Flux」— AIが賛否＋結論を生成 |
| AIコンテンツ生成 | ツイート、スレッド、Instagram、ブログ、LinkedIn原稿の自動作成（5種） |
| スマートアラート | ウォッチリストキーワード検出時にデスクトップ通知 |
| ツール比較 | 19のAIツールをカテゴリ別にニュース言及量＋感情チャートで比較 |
| トレンドチャート | キーワード別時系列チャート＋急上昇キーワード |

### 共有＋エクスポート
| 機能 | 説明 |
|------|------|
| SNS自動投稿 | X、Telegram、Discord、Threads、Instagramにカードニュースを投稿 |
| カードニュース | 1080x1080カード画像自動生成（ダークテーマ、カテゴリ別カラー） |
| エクスポート | Markdown / PDF ダウンロード |

### デスクトップ＋自動化
| 機能 | 説明 |
|------|------|
| デスクトップアプリ | ネイティブウィンドウ（pywebview）＋ システムトレイ ＋ バックグラウンド通知 |
| GitHub Actions | 1日3回自動収集・処理（CI/CD） |
| ワンクリックパイプライン | 収集→AI処理→ブリーフィング生成を一括実行 |
| リリース追跡 | 主要AIツールの新バージョン・更新情報を自動監視 |
| 自動翻訳 | ニュース記事の多言語翻訳対応 |

---

## 74のニュースソース

| カテゴリ | 件数 | 例 |
|----------|------|-----|
| 一般AI | 26 | TechCrunch, The Verge, MIT Tech Review, Wired, ZDNET, Ben's Bites |
| 画像/動画 | 20 | Stability AI, Civitai, Runway, Reddit (StableDiffusion, midjourney, flux_ai, comfyui) |
| バイブコーディング | 19 | Cursor, GitHub, Anthropic, Simon Willison, Reddit (vibecoding, ClaudeAI, cursor) |
| オントロジー | 9 | Neo4j, Stardog, W3C, Reddit (semanticweb, KnowledgeGraphs) |

---

## 35のLLMプラットフォーム

APIキーは**どれか1つ**だけで動作します：

| ティア | プラットフォーム |
|--------|-----------------|
| **無料（推奨）** | Gemini, Groq, Cerebras, SambaNova, xAI, Mistral, Cohere, HuggingFace, NVIDIA, Cloudflare, Zhipu, Kluster, GLHF, Hyperbolic |
| **クレジット / 低価格** | Together AI, OpenRouter, Fireworks, DeepSeek, DeepInfra, Perplexity, AI21, Upstage, Lepton, Novita, Nebius, Chutes, Replicate, Alibaba, Moonshot, Yi, Baichuan |
| **プレミアム** | OpenAI, Azure OpenAI, Anthropic Claude, Reka AI |

---

## はじめ方（完全初心者向け）

> **プログラミング経験は不要です。** 一つずつ順番に進めてください。

### ステップ1：Pythonインストール

1. [python.org/downloads](https://www.python.org/downloads/) にアクセス
2. 大きな黄色い **"Download Python"** ボタンをクリック
3. ダウンロードしたファイルを実行
4. **重要：** 下部の **"Add Python to PATH"** を必ずチェック！
5. **"Install Now"** をクリック

**確認：** コマンドプロンプト（`Win + R` > `cmd` > Enter）で：
```
python --version
```
`Python 3.13.x` のように表示されればOKです。

### ステップ2：プロジェクトのダウンロード

**方法A：Git（推奨）**
```
git clone https://github.com/sodam-ai/ai-news-radar.git
cd ai-news-radar
```

**方法B：直接ダウンロード**
1. [GitHubページ](https://github.com/sodam-ai/ai-news-radar) にアクセス
2. 緑色の **"Code"** ボタン > **"Download ZIP"** をクリック
3. ZIPファイルを解凍

### ステップ3：パッケージインストール

プロジェクトフォルダでコマンドプロンプトを開き：
```
pip install -r requirements.txt
```
14個のパッケージが自動インストールされます。完了まで待ちます。

### ステップ4：APIキーの取得（無料）

**Groq推奨（最も簡単）：**
1. [console.groq.com/keys](https://console.groq.com/keys) にアクセス
2. Googleアカウントで登録
3. **"Create API Key"** をクリック
4. キーをコピー（`gsk_` で始まります）

### ステップ5：APIキーの設定

1. プロジェクトフォルダの `.env.example` を見つける
2. コピーして名前を `.env` に変更
3. メモ帳で `.env` を開く
4. キーを入力：
```
GROQ_API_KEY=gsk_ここに実際のキーを入力
```
5. 保存して閉じる

> **セキュリティ：** `.env` ファイルはGitHubに自動的に除外されます。絶対に共有しないでください。

### ステップ6：アプリの起動

**Webモード（ブラウザ）：**
```
streamlit run app.py
```
ブラウザが **http://localhost:6601** を自動的に開きます。

**デスクトップモード（ネイティブウィンドウ）：**
```
python desktop.py
```
または `AI_News_Radar.bat` をダブルクリック

### ステップ7：初回使用

1. サイドバーの **「収集」** をクリック → 74ソースからニュース収集
2. **「AI処理」** をクリック → 全記事をAI分析
3. **「ブリーフィング生成」** をクリック → 今日のTOP 5を生成
4. ダッシュボードで自由に探索！

---

## 使い方ガイド

| やりたいこと | 方法 |
|------------|------|
| 今日の要約を見る | Dashboardタブ > ブリーフィング |
| 画像/動画ニュースだけ見る | Dashboardタブ > カテゴリ選択 |
| 特定テーマを検索 | News Feedタブ > 検索ビュー > キーワード入力 |
| AIに質問 | AIタブ > チャット > 質問入力 |
| AIツールを比較 | Insightsタブ > ツール比較 |
| トレンドを見る | Insightsタブ > トレンド |
| SNSコンテンツ生成 | Shareタブ > コンテンツ生成 > 記事+プラットフォーム選択 |
| SNSに投稿 | Shareタブ > SNS投稿 > プラットフォーム選択 > 投稿 |
| 音声で聴く | Dashboardタブ > 音声選択 > 「音声」クリック |
| PDFエクスポート | Shareタブ > エクスポート |
| 記事を保存 | News Feedタブ > 記事の☆をクリック |
| キーワード追跡 | サイドバー > ウォッチリスト > キーワード入力 |

---

## プロジェクト構成

```
ai-news-radar/          （ソース74個 / モジュール24個 / コミット36個）
├── app.py                    # メインダッシュボード（5タブ）
├── desktop.py                # デスクトップアプリ（pywebview + トレイ）
├── config.py                 # 設定（9カテゴリ、3感情）
├── requirements.txt          # 14パッケージ
├── ai/                       # AIモジュール群
│   ├── model_router.py       #   35 LLMプロバイダー
│   ├── briefing.py           #   デイリー＋関心分野ブリーフィング
│   ├── chat.py               #   AIニュースチャット
│   ├── voice_briefing.py     #   TTS音声（edge-tts）
│   ├── factcheck.py          #   複数ソース照合
│   ├── glossary.py           #   AI用語辞典
│   ├── weekly_report.py      #   週間インテリジェンスレポート
│   ├── competitor.py         #   19ツール監視
│   ├── trend.py              #   キーワードトレンド分析
│   ├── debate.py             #   AIディベート
│   └── smart_alert.py        #   デスクトップ通知
├── sns/                      # SNSモジュール
│   ├── card_generator.py     #   カードニュース画像（Pillow）
│   ├── poster.py             #   5プラットフォームアダプター
│   ├── content_generator.py  #   AIコンテンツ（5種）
│   └── newsletter.py         #   メールニュースレター（SMTP）
├── bot/telegram_bot.py       # Telegramボット（7コマンド）
├── scripts/                  # CLIツール
├── .github/workflows/        # GitHub Actions（1日3回）
├── crawler/                  # RSS収集（並列クローリング）
├── reader/                   # 広告なし記事リーダー
├── export/                   # Markdown + PDFエクスポート
├── data/                     # 74プリセットソース
└── PRD/                      # 設計ドキュメント
```

---

## トラブルシューティング

| 問題 | 解決方法 |
|------|----------|
| `pip` が見つからない | Python再インストール時に「Add to PATH」をチェック |
| `streamlit` が見つからない | `pip install streamlit` を実行 |
| 「APIキー未設定」の警告 | `.env` ファイルにAPIキーを入力 |
| 記事が表示されない | 「収集」→「AI処理」の順にクリック |
| カテゴリフィルターで0件 | `python scripts/reclassify.py` で既存記事を再分類 |
| ポート使用中 | `streamlit run app.py --server.port 7429` を使用 |
| PDFエクスポート失敗 | Windows専用（韓国語フォント使用） |

---

## ロードマップ

| Phase | 機能 | 状態 |
|-------|------|------|
| Phase 1 | 収集＋AI要約＋ダッシュボード（17機能） | **完了** |
| Phase 2-A | 検索＋ブックマーク＋感情分析＋チャット（5機能） | **完了** |
| Phase 2-B | 音声＋Telegram＋ファクトチェック＋用語辞典＋Actions（5機能） | **完了** |
| Tier 1 | 関心分野ブリーフィング＋週間レポート＋ツール比較（3機能） | **完了** |
| Tier 2 | トレンドチャート＋AIディベート（2機能） | **完了** |
| S-Tier | スマートアラート＋コンテンツ生成＋ニュースレター＋SNS（4機能） | **完了** |
| UI/UX | 5タブリデザイン＋ページネーション＋プレミアムCSS | **完了** |
| Desktop | pywebview＋システムトレイ＋通知 | **完了** |
| Next | 自動翻訳、ChromaDB、Ollama、ゲーミフィケーション | 予定 |

---

## 技術スタック

| コンポーネント | 技術 |
|--------------|------|
| 言語 | Python 3.11+ |
| ダッシュボード | Streamlit |
| AI | 35 LLMプラットフォーム |
| チャート | Plotly |
| 音声 | edge-tts（Microsoft TTS） |
| 画像 | Pillow（カードニュース） |
| デスクトップ | pywebview + pystray |
| ボット | python-telegram-bot |
| SNS | tweepy (X), Telegram API, Discord Webhook, Threads API, Instagram Graph API |
| CI/CD | GitHub Actions |
| データ | ローカルJSON |

---

## ライセンス

MIT License - Copyright (c) 2026 **SoDam AI Studio**

詳細は [LICENSE](./LICENSE) を参照してください。

---

*Streamlit + 35のAIプラットフォームで構築 — SoDam AI Studio*
