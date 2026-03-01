# 成長率分析ガイド

## 📊 成長率分析の実装内容

**分析手法:**
- **直近7日平均** vs **過去60日平均** の比較
- 成長率 = `((直近7日平均 - 過去60日平均) / 過去60日平均) × 100`

**除外ワード（常連・基礎用語）:**
- Artificial_intelligence
- ChatGPT
- OpenAI
- Llama_(language_model)
- Large_language_model
- Machine_learning

**対象キーワード（30個）:**
- GPT-4, Claude, Gemini, Midjourney, Stable Diffusion等の各種AIツール
- Anthropic, Google DeepMind等のAI企業
- RAG, Fine-tuning等の技術用語
- Perplexity.ai, Mistral AI, Grok等の新興サービス

---

## 🚀 使用方法

### オプション1: 60日分の履歴データ収集（初回のみ）

**⚠️ 約2時間かかります（3,600 APIリクエスト）**

```bash
cd C:\Users\Tenormusica\ai-trend-daily
python src/collect_historical_data.py
```

**実行内容:**
- 過去60日分のデータを1日ずつ収集
- 30キーワード × 60日 = 1,800データポイント
- Wikipedia Pageviews APIに順次リクエスト
- データベースに時系列で保存

**完了後:**
```bash
python src/calculate_growth.py
```

成長率Top10が表示されます。

---

### オプション2: 通常運用（60日後から自動有効化）

**現在の設定:**
- 3時間ごとに自動データ収集
- データ保持期間: 60日
- 60日経過後、自動的に成長率分析が可能に

**60日後の自動実行:**
```bash
# 自動更新スクリプト（既に設定済み）
python auto_update.py
```

実行内容:
1. 最新データ収集
2. 成長率計算（直近7日 vs 過去60日）
3. Top 10抽出
4. JSON/HTML生成

---

## 📈 出力ファイル

### JSON形式: `output/ranking.json`
```json
{
  "updated_at": "2025-10-23 22:30:00",
  "analysis_type": "growth_rate",
  "period": "Recent 7 days vs Past 60 days average",
  "ranking": [
    {
      "rank": 1,
      "keyword": "Grok (chatbot)",
      "growth_rate": 127.5,
      "recent_avg": 4500,
      "baseline_avg": 1980
    }
  ]
}
```

### HTML形式: `output/ranking.html`
- 美麗グラデーションデザイン
- 成長率を緑（上昇）/赤（下降）で色分け
- 直近7日平均ビュー数も表示
- レスポンシブ対応

---

## 🔍 データベース確認

### 収集済みデータ数確認:
```bash
cd ai-trend-daily
sqlite3 data/trends.db "SELECT COUNT(*), MIN(collected_at), MAX(collected_at) FROM trends;"
```

### キーワード別データ数:
```bash
sqlite3 data/trends.db "SELECT keyword, COUNT(*) as count FROM trends GROUP BY keyword ORDER BY count DESC;"
```

### 成長率計算可能かチェック:
```bash
sqlite3 data/trends.db "SELECT COUNT(DISTINCT DATE(collected_at)) as days FROM trends;"
```

60以上なら成長率分析可能。

---

## ⚡ クイックテスト（少量データ）

テスト用に7日分だけ収集:

```python
# collect_historical_data.py の最終行を変更
collect_historical_data(7)  # 60 → 7
```

実行:
```bash
python src/collect_historical_data.py
python src/calculate_growth.py
```

約7分で完了（210リクエスト）。

---

## 📊 現在の状態

**収集済みデータ:**
- 1日分（2025-10-23）のデータのみ
- 30キーワード × 1日 = 30データポイント

**成長率分析:**
- ❌ 現時点では不可（データ不足）
- ✅ 60日後から自動的に有効化

**絶対ページビュー数ランキング（現在利用可能）:**
1. Meta AI - 7,109 views
2. Anthropic - 6,748 views
3. Generative AI - 5,355 views
4. Sora - 3,972 views
5. Grok - 3,863 views

---

## 🛠️ トラブルシューティング

### "Insufficient data" エラー
- 成長率計算に必要な日数が不足
- 最低でも30日分のデータが必要
- 履歴データ収集を実行: `python src/collect_historical_data.py`

### API Rate Limit (429エラー)
- Wikipedia APIの制限に到達
- 自動的に0.2秒間隔で制御済み
- エラー発生時は1時間待機してから再実行

### データベースロック
- 複数プロセスが同時実行されている
- プロセス確認: `tasklist | findstr python`
- 不要なプロセス終了後に再実行

---

## 📅 推奨運用フロー

### 初回セットアップ（今日）:
1. ✅ プロジェクト作成完了
2. ✅ 3時間ごと自動収集設定完了
3. ✅ 成長率分析コード実装完了

### 60日後（自動有効化）:
- 自動的に成長率分析が開始
- Top 10が `output/ranking.html` に表示
- 3時間ごとに自動更新

### 即座に成長率分析が必要な場合:
```bash
# 過去60日分を一括収集（約2時間）
python src/collect_historical_data.py
```
