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

## ライセンス

MIT License
