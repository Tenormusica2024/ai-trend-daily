# AI Trend Daily - Project CLAUDE.md

## 🧠 AI情報ソース参照ルール

**🚨 MANDATORY: 以下のキーワードを含む質問ではWebSearch前に必ず参照**

### 発火キーワード（1つでも含めば発火）:
- AI / 人工知能 / LLM / GPT / Claude / Gemini / Grok / Llama
- 最新 / 最近 / 動向 / トレンド / ニュース / 話題
- できること / 新機能 / アップデート / リリース / 発表
- Tips / 活用 / 使い方 / プロンプト / コツ
- マネタイズ / 収益化 / 稼ぐ / 副業 / アプリ / SaaS / 売上 / 個人開発 / 壁打ち / ブレスト / アイデア

### 必須参照先（WebSearch前に絶対読む）:
| ファイル | 内容 | 更新頻度 |
|---------|------|---------|
| `D:\antigravity_projects\VaultD\Projects\Monetization\Intelligence\AI_Frontier_Capabilities_Master.md` | AIニュース・能力境界 | 毎日06:00 JST |
| `D:\antigravity_projects\VaultD\Projects\Monetization\Intelligence\AI_Knowledge_Tips_Master.md` | AI活用Tips・ナレッジ | 毎日06:30 JST |
| `D:\antigravity_projects\VaultD\Projects\Monetization\Intelligence\AI_Monetization_Radar_Master.md` | 法人向けマネタイズ・VC動向 | 定期更新 |
| `D:\antigravity_projects\VaultD\Projects\Monetization\Intelligence\AI_Monetization_Radar_Individual.md` | 個人向けマネタイズ・ツール開発・マーケ | 定期更新 |

### 発火例:
「最近のAI動向は？」「GPT-5出た？」「Claudeの新機能ある？」「AIの使い方教えて」「AIで稼ぐ方法は？」「マネタイズできる？」

---

## 📁 プロジェクト情報

### リポジトリ
- **GitHub**: https://github.com/Tenormusica2024/ai-trend-daily
- **GitHub Pages**: https://tenormusica2024.github.io/ai-trend-daily/
- **ローカルパス**: `C:\Users\Tenormusica\ai-trend-daily\`

### 概要
Wikipedia Pageviews API（英語版・日本語版）を使用して、AI関連キーワードの1週間急上昇率Top20を自動更新するツール。

---

## ⏰ 定期更新スケジュール（Task Scheduler）

### ランキング更新タスク
| タスク名 | 実行時刻 | 対象スクリプト | 出力ファイル |
|---------|---------|---------------|-------------|
| `GitHub_Trend_Ranking_Daily_Update` | 09:00 JST | `update_github_ranking.py` | `github_ranking.json` |
| `AI-Trend-Daily-Image-Ranking-Update` | 03:00 JST | `update_image_ranking.py` | `image_ranking.json` |
| `AI_Video_Ranking_Daily_Update` | 03:00 JST | `update_video_ranking.py` | `video_ranking.json` |

### AI情報収集タスク（関連）
| タスク名 | 実行時刻 | 説明 |
|---------|---------|------|
| `AI_Frontier_Intelligence_Daily` | 06:00 JST | AI最新ニュース収集 → Obsidian Vault保存 |
| `AI_Knowledge_Daily` | 06:30 JST | AI活用Tips更新 |
| `AI-Monetization-Daily` | 定期 | マネタイズ情報更新 |

---

## 📂 ファイル構成

### 出力ファイル（GitHub Pagesで公開）
```
ai-trend-daily/
├── index.html                  # メインページ（急上昇ランキング）
├── github-trend-ranking.html   # GitHubトレンドランキング
├── image-ai-ranking.html       # 画像AI関連ランキング
├── video-ai-ranking.html       # 動画AI関連ランキング
├── home.html                   # ホームページ
├── github_ranking.json         # GitHubランキングデータ
├── image_ranking.json          # 画像ランキングデータ
├── video_ranking.json          # 動画ランキングデータ
└── docs/
    └── surge_ranking.json      # 急上昇ランキングJSON
```

### 実行スクリプト
```
├── update_github_ranking.py         # GitHubランキング更新
├── update_image_ranking.py          # 画像ランキング更新
├── update_video_ranking.py          # 動画ランキング更新
├── update_github_ranking_daily.bat  # Task Scheduler用バッチ
├── update_image_ranking_daily.bat   # Task Scheduler用バッチ
├── update_video_ranking_daily.bat   # Task Scheduler用バッチ
└── update_ranking_common.bat        # 共通バッチ処理
```

### ログファイル
```
logs/
├── github_ranking_YYYYMMDD.log
├── image_ranking_YYYYMMDD.log
└── video_ranking_YYYYMMDD.log
```

---

## 🔧 トラブルシューティング

### Task Scheduler エラーコード
| コード | 意味 | 解決策 |
|--------|------|--------|
| 0 | 正常終了 | 問題なし |
| 1 | 一般エラー | ログ確認 |
| 9009 | コマンド未検出 | Pythonフルパス指定 |
| 4 | git push失敗 | 認証確認 |

### ログ確認コマンド
```powershell
# 最新ログを確認
Get-Content "C:\Users\Tenormusica\ai-trend-daily\logs\github_ranking_$(Get-Date -Format 'yyyyMMdd').log"
```

### 手動テスト実行
```powershell
schtasks /run /tn "\GitHub_Trend_Ranking_Daily_Update"
```

---

## 🔗 関連リソース

### Obsidian Vault（AI情報ソース）
- **パス**: `D:\antigravity_projects\VaultD\Projects\Monetization\Intelligence\`
- **ファイル**:
  - `AI_Frontier_Capabilities_Master.md` - AIニュース・能力境界
  - `AI_Knowledge_Tips_Master.md` - AI活用Tips
  - `AI_Monetization_Radar_Master.md` - 法人向けマネタイズ
  - `AI_Monetization_Radar_Individual.md` - 個人向けマネタイズ

### 関連スキル
- **ai-frontier-intelligence**: `C:\Users\Tenormusica\.claude\skills\ai-frontier-intelligence\`
  - 毎日06:00 JSTに自動実行
  - Claude Code + Task Scheduler

---

## 📊 技術スタック

- Python 3.x
- Wikipedia Pageviews API
- Gemini API（翻訳機能）
- SQLite（履歴データ管理）
- GitHub Pages（公開）
- Windows Task Scheduler（自動実行）
