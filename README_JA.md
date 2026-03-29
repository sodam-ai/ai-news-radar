# AI News Radar

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-SoDam%20AI%20Studio-green)
![Release](https://img.shields.io/badge/Release-v1.1.0-blue)

[English](README.md) | [한국어](README_KO.md) | [日本語](README_JA.md) | [中文](README_ZH.md)

---

**AI News Radar**は、**74のニュースソース**からAI関連ニュースを自動収集し、AIが要約・分類・分析する個人向けニュースプラットフォームです。

---

## 実行方法（3ステップ）

> **プログラミング経験は一切不要です。** 以下の3ステップに従うだけです。

### ステップ1：ダウンロード

このページ上部の緑色の **「Code」** ボタンをクリックし、**「Download ZIP」** をクリックします。

ダウンロードしたZIPファイルを任意のフォルダに解凍します。

### ステップ2：Pythonのインストール

既にPythonがインストールされている場合は、このステップをスキップしてください。

1. **[python.org/downloads](https://www.python.org/downloads/)** にアクセス
2. 黄色の **「Download Python」** ボタンをクリック
3. ダウンロードしたファイルを実行
4. **重要：画面下部の「Add Python to PATH」にチェックを入れてください！**
5. **「Install Now」** をクリック

### ステップ3：アプリの起動

解凍したフォルダを開き、以下のファイルを**ダブルクリック**します：

| ファイル | 説明 |
|---------|------|
| **`install_and_run.bat`** | **初回起動時に使用。** すべてを自動インストールし、APIキーの設定を案内します。 |
| **`start.bat`** | **2回目以降に使用。** 素早く起動します。 |

以上です！ブラウザにAI News Radarが表示されます。

---

## 無料APIキーの取得

AI News Radarがニュースを分析するには、AIサービスが必要です。**Google Gemini**（無料）を推奨します。

1. **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)** にアクセス
2. Googleアカウントでログイン
3. **「Create API Key」** をクリック
4. キーをコピー

`install_and_run.bat`を実行すると、自動的にキーの入力を案内します。

> **35のAIサービスに対応。** `.env.example`で全リストを確認できます。キーは1つだけでOKです。

---

## 主な機能（45以上）

### ニュース収集
- **74のRSSソース**から自動収集（英語＋韓国語）
- 重複ニュースの自動統合
- キーワードウォッチリスト
- 英語記事の自動韓国語翻訳

### AI分析
- **ワンクリックパイプライン**：収集→分析→ブリーフィングを一括実行
- 毎日TOP5ブリーフィング自動生成
- 週間インテリジェンスレポート
- AIチャット（ニュースについて質問）
- トレンド分析＋チャート
- AIツールリリース追跡
- 競合ツール比較
- AIディベートモード（賛否分析）
- AI用語辞典
- ファクトチェック
- スマートアラート

### コンテンツ＆共有
- 音声ブリーフィング（TTS）
- Markdown / PDFエクスポート
- Discord、Telegram、X、Threads、Instagramへの投稿
- AIコンテンツ自動生成
- メールニュースレター配信

---

## 環境変数

すべての設定は`.env`ファイルに保存されます。最低1つのAPIキーが必要です。

| 変数 | 必須 | 説明 |
|------|------|------|
| `GEMINI_API_KEY` | 推奨 | Google Gemini（無料：1000回/日） |
| `GROQ_API_KEY` | 代替 | Groq（無料：14,400回/日） |
| `OPENAI_API_KEY` | 代替 | OpenAI GPT（有料） |

---

## よくある質問

**Q：「API key not configured」と表示されます**
A：`.env`ファイルをメモ帳で開き、APIキーが正しく入力されているか確認してください。

**Q：.batファイルをダブルクリックしても何も起きません**
A：.batファイルを右クリック→「管理者として実行」を選択してください。

**Q：MacやLinuxでも使えますか？**
A：はい！ターミナルで以下のコマンドを実行してください：
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 6601
```

---

## ライセンス

Copyright (c) 2026 **SoDam AI Studio**. All rights reserved.

本ソフトウェアは個人利用および教育目的で提供されています。商用利用についてはパブリッシャーにお問い合わせください。
