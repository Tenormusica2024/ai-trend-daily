# GitHub Trend Ranking System

## 概要

GitHubのトレンドリポジトリを毎日自動収集してランキング化するシステムです。  
各リポジトリの日本語説明、使用言語、スター数、プロジェクトの概要を表示します。

**公開URL**: https://tenormusica2024.github.io/ai-trend-daily/

## システム構成

### 1. フロントエンド（HTML/CSS/JavaScript）

#### index.html
- GitHub トレンドランキング表示ページ
- ダークグラデーション背景のモダンなUI
- レスポンシブデザイン（デスクトップ/モバイル対応）
- 10分ごとの自動リフレッシュ機能

#### github-trend-ranking.html
- オリジナルのHTMLテンプレート（バックアップ用）

#### index_backup_wikipedia.html
- 元のWikipediaキーワードランキングのバックアップ

### 2. バックエンド（Python）

#### update_github_ranking.py
- GitHub trending ページのスクレイピングスクリプト
- **主な機能**:
  - BeautifulSoup4 でHTML解析
  - リポジトリ名、説明、言語、スター数を抽出
  - 上位15件のトレンドリポジトリを取得
  - **Gemini API による自動翻訳機能**（2025-10-29追加）
  - JSONファイルに保存
  - Windows console エンコーディング対応（UTF-8/cp932）

**主要な関数**:
```python
fetch_github_trending()   # GitHub trending ページを取得
parse_trending_repos()    # HTML を解析してリポジトリデータを抽出
translate_to_japanese()   # Gemini API で英語説明文を日本語に翻訳（NEW）
create_ranking_json()     # ランキングJSONデータを作成
save_json()               # JSONファイルに保存
```

**翻訳機能の詳細（2025-10-29実装）**:
- **使用API**: Google Gemini 2.0 Flash Exp
- **APIキー**: 環境変数または設定ファイルから取得
- **翻訳プロンプト**:
  ```
  以下の英語のGitHubリポジトリ説明文を自然な日本語に翻訳してください。
  
  【翻訳ルール】
  1. 技術用語は適切に日本語化してください
  2. 読みやすく簡潔な表現にしてください
  3. 翻訳結果のみを出力し、説明や前置きは不要です
  4. 原文の意味を正確に伝えてください
  ```
- **レート制限対策**: 各翻訳後に0.5秒待機（10 requests/分の制限回避）
- **エラーハンドリング**: API失敗時は元の英語テキストを保持
- **トークン設定**: 
  - temperature: 0.3（一貫性重視）
  - maxOutputTokens: 200
  - responseModalities: ["TEXT"]

**モデル選定経緯**:
1. **Gemini 1.5 Flash** → 404エラー（モデル非対応）
2. **Gemini 2.5 Flash** → thinking機能でトークン消費のみ、テキスト出力なし
3. **Gemini 2.0 Flash Exp** ✅ → 成功（thinking機能なし、安定版）

**翻訳品質の改善**:
- **Before（キーワード置換）**: 英語と日本語が混在した不自然な文章
- **After（Gemini API）**: 完全に自然な日本語文章

**翻訳例**:
```
英語原文:
"There can be more than Notion and Miro. AFFiNE is a next-gen knowledge base 
that brings planning, sorting and creating all together."

日本語翻訳:
"NotionやMiroだけではありません。AFFiNEは、計画、整理、作成を統合した
次世代のナレッジベースです。プライバシーを第一に考え、オープンソースで、
カスタマイズ可能、そしてすぐに使用できます。"
```

### 3. データ（JSON）

#### github_ranking.json
- 15件のトレンドリポジトリデータ
- **データ構造**（2025-10-29更新）:
```json
{
  "updated_at": "2025-10-29 13:38:29",
  "total_repos": 15,
  "ranking": [
    {
      "rank": 1,
      "repo_name": "toeverything/AFFiNE",
      "description": "There can be more than Notion and Miro. AFFiNE is a next-gen knowledge base...",
      "description_ja": "NotionやMiroだけではありません。AFFiNEは、計画、整理、作成を統合した次世代のナレッジベースです。",
      "language": "TypeScript",
      "stars": 0
    }
  ]
}
```

**特徴**:
- **全リポジトリに日本語説明を追加**（Gemini API翻訳）
- **二重言語対応**: `description`（英語原文）と`description_ja`（日本語翻訳）の両方を保持
- 実際のスター数を含む
- UTF-8エンコーディング
- **翻訳品質**: 機械的なキーワード置換から、Gemini APIによる自然な日本語文章へ改善（2025-10-29）

### 4. 自動更新システム

#### update_github_ranking_daily.bat
- 毎日実行されるWindows バッチスクリプト
- **実行内容**:
  1. Python スクリプト実行
  2. Git add, commit, push 自動実行
  3. GitHub Pages 自動デプロイ

#### register_task.bat
- Windows Task Scheduler にタスクを登録
- **実行コマンド**:
```batch
schtasks /create /tn "GitHub_Trend_Ranking_Daily_Update" /tr "cmd.exe /c C:\Users\Tenormusica\ai-trend-daily\update_github_ranking_daily.bat" /sc daily /st 09:00 /f
```

#### check_task.bat
- 登録されたタスクの確認用スクリプト

#### setup_daily_task.ps1
- PowerShell によるTask Scheduler 設定スクリプト
- 管理者権限で実行

## 自動更新の仕組み

### データ更新フロー

1. **毎日午前9時**: Windows Task Scheduler がタスクを起動
2. **バッチ実行**: `update_github_ranking_daily.bat` が実行される
3. **スクレイピング**: Python スクリプトが GitHub trending からデータ取得
4. **JSON更新**: `github_ranking.json` が最新データで更新される
5. **Git操作**: 自動的に commit & push 実行
6. **デプロイ**: GitHub Pages が自動デプロイ
7. **完了**: ユーザーは常に最新のトレンドランキングを閲覧可能

### フロントエンド自動更新

- JavaScript `setInterval` で10分ごとにJSONデータを再読み込み
- ページを開いたままでも最新データが表示される

## UI デザイン

### デザイン特徴

- **カラースキーム**: ダークグラデーション背景
- **レスポンシブ**: デスクトップ・モバイル両対応
- **アニメーション**: ホバーエフェクト、スムーズな遷移
- **タイポグラフィ**: システムフォント（San Francisco/Segoe UI/Roboto）

### グリッドレイアウト

**デスクトップ**:
```
60px (ランク番号) | 1fr (リポジトリ情報) | 120px (スター数)
```

**モバイル**:
```
50px (ランク番号) | 1fr (リポジトリ情報 + スター数)
```

### 表示項目

- **ランク番号**: #1〜#15（青色、大きなフォント）
- **リポジトリ名**: GitHub へのリンク付き
- **日本語説明**: 各リポジトリの概要（2〜3行）
- **プログラミング言語**: タグ表示
- **スター数**: 星アイコン付き（オレンジ色）

## トレンドリポジトリ例（2025-10-27時点）

1. **LadybirdBrowser/ladybird** (C++, 53,714 stars)  
   完全に独立したウェブブラウザプロジェクト。既存のブラウザエンジンに依存せず、ゼロから構築された真の独立ブラウザを目指している。

2. **yeongpin/cursor-free-vip** (Python, 37,925 stars)  
   Cursor AI の MachineID リセットとトークン制限バイパスをサポートするツール。0.49.x バージョンに対応し、無料で VIP 機能を利用可能にする。

3. **cjpais/Handy** (TypeScript, 3,482 stars)  
   完全にオフラインで動作する無料のオープンソース音声認識アプリケーション。拡張可能な設計で、インターネット接続なしで音声をテキストに変換できる。

4. **Shubhamsaboo/awesome-llm-apps** (Python, 73,212 stars)  
   OpenAI、Anthropic、Gemini、オープンソースモデルを使用した AI エージェントと RAG を備えた LLM アプリのコレクション。実用的な AI アプリケーション例を多数収録。

5. **microsoft/agent-lightning** (Python, 2,372 stars)  
   AI エージェントのトレーニングを効率化する Microsoft の絶対的トレーナー。エージェントの開発とデプロイを高速化するためのツールセット。

## 技術的詳細

### スクレイピング

- **対象URL**: https://github.com/trending
- **ライブラリ**: 
  - `beautifulsoup4`: HTML解析
  - `requests`: HTTP通信
- **取得データ**: リポジトリ名、説明、言語、スター数
- **対応リポジトリ数**: 上位15件

### データ形式

- **フォーマット**: JSON（UTF-8エンコーディング）
- **構造**: 
  - `updated_at`: 更新日時
  - `total_repos`: リポジトリ総数
  - `ranking`: ランキング配列
- **特徴**: 全リポジトリに日本語説明を追加

### 自動化

- **スケジューラー**: Windows Task Scheduler
- **実行時刻**: 毎日午前9時00分
- **Git操作**: 自動コミット・プッシュ
- **デプロイ**: GitHub Pages 自動デプロイ

### エンコーディング対応

- Windows console (cp932) エンコーディング問題を修正
- UTF-8で正常に動作
- Unicode文字（絵文字等）を適切に処理

## セットアップ手順

### 1. 依存関係のインストール

```bash
pip install beautifulsoup4 requests
```

### 2. Task Scheduler 登録

**方法1: バッチファイル実行**
```batch
cd C:\Users\Tenormusica\ai-trend-daily
register_task.bat
```

**方法2: PowerShell実行（管理者権限）**
```powershell
cd C:\Users\Tenormusica\ai-trend-daily
.\setup_daily_task.ps1
```

### 3. タスク確認

```batch
cd C:\Users\Tenormusica\ai-trend-daily
check_task.bat
```

**出力例**:
```
フォルダ: \
タスク名                                 次回の実行時刻         状態           
======================================== ====================== ===============
GitHub_Trend_Ranking_Daily_Update        2025/10/28 9:00:00     準備完了
```

## 手動実行方法

### Python スクリプト単体実行

```bash
cd C:\Users\Tenormusica\ai-trend-daily
python update_github_ranking.py
```

### バッチファイル実行（Git操作含む）

```batch
cd C:\Users\Tenormusica\ai-trend-daily
update_github_ranking_daily.bat
```

### Task Scheduler から手動実行

```powershell
Start-ScheduledTask -TaskName "GitHub_Trend_Ranking_Daily_Update"
```

## トラブルシューティング

### タスクが実行されない

**確認事項**:
1. Task Scheduler にタスクが登録されているか確認
   ```batch
   check_task.bat
   ```

2. タスクの状態を確認
   - 「準備完了」になっているか
   - 次回実行時刻が正しいか

3. 手動実行でエラーが出ないか確認
   ```batch
   update_github_ranking_daily.bat
   ```

### スクレイピングエラー

**考えられる原因**:
- GitHub trending のHTML構造が変更された
- インターネット接続の問題
- User-Agent のブロック

**対処方法**:
1. Python スクリプトを手動実行してエラー内容を確認
2. HTML構造の変更に合わせてスクリプトを修正
3. User-Agent を更新

### エンコーディングエラー

**症状**:
- 日本語が文字化けする
- コンソール出力でエラーが発生

**対処方法**:
- `update_github_ranking.py` のエンコーディング処理を確認
- Windows console のコードページを確認（`chcp` コマンド）

## メンテナンス

### 定期的な確認項目

1. **タスク実行状況**:
   - Task Scheduler でタスクが正常に実行されているか確認
   - 実行履歴を確認

2. **データ更新**:
   - `github_ranking.json` の更新日時を確認
   - GitHub Pages で最新データが表示されているか確認

3. **HTML構造変更**:
   - GitHub trending のページ構造が変更されていないか確認
   - スクレイピングが正常に動作しているか確認

### ログ確認

**バッチファイル実行時のコンソール出力**:
```
============================================================
GitHub Trend Ranking Daily Update
============================================================
Started at: 2025/10/27 12:11:08

[1/3] Fetching GitHub trending page...
[2/3] Parsing repository data...
Found 15 trending repositories
[3/3] Creating JSON file...
Saved: github_ranking.json

============================================================
GitHub Trend Ranking Update Complete!
============================================================
Updated at: 2025-10-27 12:11:10
Total repositories: 15

Top 5 Repositories:
  #1 LadybirdBrowser/ladybird (53,714 stars)
  #2 yeongpin/cursor-free-vip (37,925 stars)
  #3 cjpais/Handy (3,482 stars)
  #4 Shubhamsaboo/awesome-llm-apps (73,212 stars)
  #5 microsoft/agent-lightning (2,372 stars)
```

## システムの利点

### ユーザーにとっての利点

- **最新情報**: 毎日自動的に最新のGitHubトレンドを取得
- **日本語対応**: 各リポジトリの内容を日本語で理解できる
- **使いやすいUI**: モダンで見やすいデザイン
- **完全自動化**: 手動作業不要

### 技術的利点

- **完全自動化**: データ更新からデプロイまで自動
- **高速・安定**: GitHub Pages で静的ホスティング
- **レスポンシブ**: モバイルデバイスでも快適に閲覧
- **リアルタイム更新**: 10分ごとの自動リフレッシュ

## ファイル構成

```
ai-trend-daily/
├── index.html                        # メインページ（GitHub Trend Ranking）
├── github-trend-ranking.html         # HTMLテンプレート（バックアップ）
├── index_backup_wikipedia.html       # 元のWikipediaランキング（バックアップ）
├── github_ranking.json               # トレンドリポジトリデータ
├── update_github_ranking.py          # スクレイピングスクリプト
├── update_github_ranking_daily.bat   # 毎日実行バッチ
├── register_task.bat                 # Task Scheduler 登録
├── check_task.bat                    # Task Scheduler 確認
├── setup_daily_task.ps1              # PowerShell 設定スクリプト
└── GITHUB_TREND_RANKING.md           # 本ドキュメント
```

## Git コミット情報

- **Repository**: Tenormusica2024/ai-trend-daily
- **Commit**: 711c858
- **Branch**: main
- **Files**: 7 files changed, 1167 insertions(+), 58 deletions(-)

## ライセンス

このプロジェクトは MIT License のもとで公開されています。

## 更新履歴

- **2025-10-29**: Gemini API 翻訳機能実装
  - Gemini 2.0 Flash Exp による高品質な日本語翻訳機能追加
  - キーワード置換から完全な文章翻訳への改善
  - レート制限対策（0.5秒待機）実装
  - 二重言語対応（`description`と`description_ja`）
  - モデル選定: 1.5 Flash → 2.5 Flash → 2.0 Flash Exp
  - エラーハンドリングとフォールバック機能追加
  - 翻訳品質の大幅向上（自然な日本語文章）

- **2025-10-27**: GitHub Trend Ranking システム実装完了
  - HTML ページ作成
  - Python スクレイピングスクリプト作成
  - 自動更新システム構築
  - Task Scheduler 登録
  - GitHub Pages デプロイ

---

**最終更新**: 2025-10-29  
**次回自動更新**: 2025-10-30 09:00:00  
**翻訳機能**: Gemini 2.0 Flash Exp（2025-10-29実装）
