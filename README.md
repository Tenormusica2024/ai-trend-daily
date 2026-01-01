# AI Trend Keywords - Weekly Surge Ranking 🚀

Wikipedia APIを活用したAI関連トレンドワードの自動追跡・急上昇検出システム

## 🌐 ライブランキング

**👉 [AI Trend Keywords - Weekly Surge Ranking](https://tenormusica2024.github.io/ai-trend-daily/)**

## 概要

Wikipedia Pageviews API（英語版・日本語版）を使用して、AI関連キーワードの1週間急上昇率Top20を3時間ごとに自動更新するツールです。

## 機能

- 📊 Wikipedia Pageviews API（en.wikipedia + ja.wikipedia）からAI関連キーワードのアクセス数を取得
- 📈 1週間急上昇率Top20を3時間ごとに自動更新
- 🗄️ SQLiteデータベースで履歴データを管理（7日間）
- 🌐 GitHub Pagesでリアルタイムランキング可視化
- 🎯 除外ワード機能（ChatGPT、Claude、GPT-4など25個の一般的AI用語を除外）
- 🔄 直近3日平均 vs 過去7日平均の比較で急成長を検出

## 技術スタック

- Python 3.x
- Wikipedia Pageviews API
- SQLite
- Windows Task Scheduler

## 自動更新スケジュール

- 更新頻度: 3時間ごと（0時、3時、6時、9時、12時、15時、18時、21時）
- データ保持: 7日間の履歴データ

## セットアップ

```bash
# リポジトリクローン
git clone https://github.com/Tenormusica2024/ai-trend-daily.git
cd ai-trend-daily

# 依存パッケージインストール
pip install -r requirements.txt

# 初回実行
python src/collect_trends.py
```

## ファイル構成

```
ai-trend-daily/
├── docs/
│   ├── index.html            # GitHub Pages公開ページ
│   └── surge_ranking.json    # 最新急上昇ランキング（JSON）
├── src/
│   ├── collect_trends.py     # Wikipedia APIデータ収集
│   ├── collect_week_data.py  # 過去7日分データ収集
│   ├── calculate_weekly_surge.py  # 急上昇率計算
│   ├── visualize_surge.py    # 急上昇ランキング可視化
│   ├── database.py           # データベース操作
│   └── config.py             # 設定ファイル（キーワード・除外ワード）
├── data/
│   └── trends.db             # SQLiteデータベース
├── auto_update.py            # 自動更新メインスクリプト
└── README.md
```

## GitHub Pages公開設定

1. GitHubリポジトリの Settings > Pages を開く
2. Source: `Deploy from a branch`
3. Branch: `main` (または `master`) / `docs` ディレクトリ
4. Save

## Task Scheduler トラブルシューティング

### エラーコード一覧

| エラーコード | 意味 | 解決策 |
|-------------|------|--------|
| **0** | 正常終了 | 問題なし |
| **1** | 一般的なエラー | Pythonスクリプトのエラー。ログを確認 |
| **-2147024894 (0x80070002)** | ファイルが見つからない | Python/batファイルのパスを確認 |
| **-1073741510 (0xC000013A)** | ユーザーによる中断 | ダイアログやブラウザが開いて中断された可能性。batファイルのgit push等を確認 |
| **9009** | コマンドが見つからない | `python`のフルパスを指定する必要あり |

### よくある問題と解決策

#### 1. Python が見つからない (Last Result: 1 or 9009)
Task Scheduler の実行環境では PATH が通っていないため、Python のフルパス指定が必須。

**修正前:**
```batch
python update_github_ranking.py
```

**修正後:**
```batch
"C:\Users\Tenormusica\AppData\Local\Programs\Python\Python310\python.exe" update_github_ranking.py
```

#### 2. 作業ディレクトリが設定されていない
batファイル内で必ず `cd /d` で作業ディレクトリを指定:
```batch
cd /d "C:\Users\Tenormusica\ai-trend-daily"
```

#### 3. タスク設定の確認方法
```powershell
# タスクの詳細情報を確認
schtasks /query /tn "\GitHub_Trend_Ranking_Daily_Update" /fo LIST /v

# 最終実行結果のみ確認
schtasks /query /tn "\GitHub_Trend_Ranking_Daily_Update" /fo LIST /v | Select-String "Last Run|Result"

# タスクのXML設定を確認
schtasks /query /tn "\GitHub_Trend_Ranking_Daily_Update" /xml
```

#### 4. タスクの再作成
```powershell
# 削除して再作成
schtasks /delete /tn "\GitHub_Trend_Ranking_Daily_Update" /f
schtasks /create /tn "GitHub_Trend_Ranking_Daily_Update" /tr "C:\Users\Tenormusica\ai-trend-daily\update_github_ranking_daily.bat" /sc daily /st 09:00 /f
```

#### 5. 手動テスト実行
```powershell
# タスクを即座に実行
schtasks /run /tn "\GitHub_Trend_Ranking_Daily_Update"
```

### 定期実行タスク一覧

| タスク名 | 実行時刻 | 対象スクリプト |
|---------|---------|---------------|
| GitHub_Trend_Ranking_Daily_Update | 09:00 | update_github_ranking.py |
| AI-Trend-Daily-Image-Ranking-Update | 03:00 | update_image_ranking.py |
| AI_Video_Ranking_Daily_Update | 03:00 | update_video_ranking.py |

### ログファイル

実行ログは `logs/` ディレクトリに日付別で保存される:
- `logs/github_ranking_YYYYMMDD.log`
- `logs/image_ranking_YYYYMMDD.log`
- `logs/video_ranking_YYYYMMDD.log`

**ログ確認コマンド:**
```powershell
# 最新ログを確認
Get-Content "C:\Users\Tenormusica\ai-trend-daily\logs\github_ranking_$(Get-Date -Format 'yyyyMMdd').log"
```

### Exit Codes

| コード | 意味 |
|--------|------|
| 0 | 正常終了 |
| 1 | ディレクトリ移動失敗 / Python実行エラー |
| 2 | git add 失敗 |
| 3 | git commit 失敗 |
| 4 | git push 失敗 |

### Gemini API レート制限 (429エラー)

翻訳機能で Gemini API を使用しているため、短時間に大量のリクエストを送るとレート制限に引っかかる場合がある。
スクリプト内でリトライ処理（最大3回）と待機時間（1-2秒）を設定済み。

## ライセンス

MIT License
