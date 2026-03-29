# note.com 自動投稿システム

## 概要

ai-trend-dailyプロジェクトで作成した技術記事をnote.comに自動投稿するシステムです。

**アカウント情報:**
- **クリエイター名**: Urayaha Days
- **note ID**: urayahadays
- **メールアドレス**: tenormusica7@gmail.com
- **パスワード**: Tbbr43gb

## ファイル構成

```
ai-trend-daily/
├── articles/                                    # 記事ディレクトリ
│   ├── coinbase-x402-protocol-analysis-2025.md
│   └── affine-notion-alternative-privacy-first-2025.md
├── note_auto_poster.py                          # 手動投稿補助スクリプト
├── note_auto_poster_playwright.py               # Playwright完全自動化スクリプト
├── note_posted_articles.json                    # 投稿済み記事ログ（自動生成）
└── NOTE_AUTO_POSTING_README.md                  # このファイル
```

## 使用方法

### 方法1: 手動投稿補助スクリプト（推奨・最も確実）

未投稿の記事リストを表示し、投稿手順を案内します。

```bash
cd C:\Users\Tenormusica\ai-trend-daily
python note_auto_poster.py
```

**特徴:**
- ✅ 確実に動作
- ✅ 投稿済み記事を自動記録
- ✅ 重複投稿を防止
- ⚠️ ブラウザでの手動操作が必要

**実行フロー:**
1. スクリプトが未投稿記事を検出
2. 記事タイトルと本文を表示
3. note.comへのログイン手順を表示
4. ユーザーがブラウザで手動投稿
5. 投稿完了後、URLを入力して記録

### 方法2: Claude Code + Playwright MCP完全自動化

Claude Codeセッション内でPlaywright MCPツールを使用して完全自動投稿します。

**前提条件:**
- Claude Code環境で実行
- Playwright MCPが有効化されていること

**実行手順:**

#### ステップ1: スクリプト実行で投稿準備

```bash
cd C:\Users\Tenormusica\ai-trend-daily
python note_auto_poster_playwright.py
```

スクリプトが未投稿記事と投稿用コマンドを表示します。

#### ステップ2: Claude CodeでPlaywright MCPツール実行

Claude Codeセッションで以下のMCPツールを順次実行：

```python
# 1. noteログインページにアクセス
mcp__playwright__playwright_navigate(url="https://note.com/login")

# 2. メールアドレス入力
mcp__playwright__playwright_fill(
    selector="input[type='email']", 
    value="tenormusica7@gmail.com"
)

# 3. パスワード入力
mcp__playwright__playwright_fill(
    selector="input[type='password']", 
    value="Tbbr43gb"
)

# 4. ログインボタンクリック
mcp__playwright__playwright_click(selector="button[type='submit']")

# 5. ページ遷移待機
import time
time.sleep(3)

# 6. 投稿ボタンをクリック
mcp__playwright__playwright_click(selector="a[href*='note/new']")

# 7. テキスト投稿を選択
mcp__playwright__playwright_click(selector="button:has-text('テキスト')")

# 8. タイトル入力
mcp__playwright__playwright_fill(
    selector="input[placeholder*='タイトル']", 
    value="記事タイトル"
)

# 9. 本文入力
mcp__playwright__playwright_fill(
    selector="textarea[placeholder*='本文']", 
    value="記事本文..."
)

# 10. 公開ボタンクリック
mcp__playwright__playwright_click(selector="button:has-text('公開')")

# 11. スクリーンショットで確認
mcp__playwright__playwright_screenshot(name="note_posted_verification")
```

**特徴:**
- ✅ 完全自動化
- ✅ スクリーンショットによる検証
- ⚠️ note.comのHTML構造変更で動作しなくなる可能性
- ⚠️ Claude Code環境が必要

### 方法3: Claude Codeに直接依頼（最もシンプル）

Claude Codeセッションで直接依頼する方法：

```
「articles/ディレクトリの未投稿記事をnote.comに投稿してください。
アカウント情報はNOTE_AUTO_POSTING_README.mdを参照。
Playwright MCPツールを使用して自動投稿を実行してください。」
```

Claude Codeが自動的に：
1. 未投稿記事を検出
2. 記事内容を読み込み
3. Playwright MCPでnote.comにログイン
4. 記事を投稿
5. 投稿済みログを更新

## 投稿済み記事ログ

`note_posted_articles.json` に投稿済み記事が記録されます。

**フォーマット:**
```json
{
  "posted": [
    {
      "file": "C:\\Users\\Tenormusica\\ai-trend-daily\\articles\\coinbase-x402-protocol-analysis-2025.md",
      "note_url": "https://note.com/urayahadays/n/n1234567890ab",
      "posted_at": "2025-10-29T18:00:00"
    }
  ]
}
```

## トラブルシューティング

### Q1: スクリプトが「記事ディレクトリが存在しません」と表示される

**A:** articlesディレクトリが正しい場所にあるか確認してください。

```bash
cd C:\Users\Tenormusica\ai-trend-daily
ls articles/
```

### Q2: 投稿済みログをリセットしたい

**A:** `note_posted_articles.json` を削除または編集してください。

```bash
# ログファイル削除（すべて未投稿扱いになる）
rm note_posted_articles.json

# または手動編集
notepad note_posted_articles.json
```

### Q3: Playwright MCPが動作しない

**A:** Claude Code環境でPlaywright MCPが有効か確認してください。

```bash
# Claude Codeで実行
mcp__playwright__playwright_navigate(url="https://note.com/")
```

エラーが出る場合は方法1（手動投稿補助）を使用してください。

### Q4: noteのセレクタが変更されてPlaywrightが動かない

**A:** note.comがHTML構造を変更した可能性があります。以下の手順で修正：

1. ブラウザでnote.comを開く
2. F12でDevToolsを開く
3. Elements タブで正しいセレクタを確認
4. `note_auto_poster_playwright.py` のセレクタを更新

## セキュリティ注意事項

⚠️ **重要**: このREADMEにはパスワードが平文で記載されています。

**推奨対策:**
1. プライベートリポジトリでのみ管理
2. 環境変数での管理に移行
3. GitHubにプッシュする前に機密情報を削除

**環境変数での管理例:**
```bash
# Windowsの場合
setx NOTE_PASSWORD "Tbbr43gb"

# Linuxの場合
export NOTE_PASSWORD="Tbbr43gb"
```

スクリプト側で環境変数から読み込み：
```python
NOTE_PASSWORD = os.getenv("NOTE_PASSWORD")
```

## 今後の改善案

- [ ] GitHub Actionsによる定期自動投稿
- [ ] 画像の自動アップロード
- [ ] ハッシュタグの自動付与
- [ ] 投稿予約機能
- [ ] note APIが公開された場合の対応

## サポート

問題が発生した場合は、GitHub Issue #1にコメントしてください。
