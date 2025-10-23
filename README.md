# AI Trend Keywords Top 10

Wikipedia APIを活用したAI関連トレンドワードの自動追跡システム

## 概要

Wikipedia Pageviews APIを使用して、AI関連キーワードのトレンドTop10を3時間ごとに自動更新するツールです。

## 機能

- Wikipedia Pageviews APIからAI関連キーワードのアクセス数を取得
- Top10ランキングを3時間ごとに自動更新
- SQLiteデータベースで履歴データを管理
- リアルタイムランキング可視化

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
├── src/
│   ├── collect_trends.py    # Wikipedia APIデータ収集
│   ├── database.py           # データベース操作
│   ├── config.py             # 設定ファイル
│   └── visualize.py          # ランキング可視化
├── data/
│   └── trends.db             # SQLiteデータベース
├── output/
│   └── ranking.json          # 最新ランキング（JSON）
├── auto_update.py            # 自動更新メインスクリプト
└── README.md
```

## ライセンス

MIT License
