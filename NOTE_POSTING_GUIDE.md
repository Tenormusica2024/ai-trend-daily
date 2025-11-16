# note.com 記事投稿手順

## アカウント情報
- **メールアドレス**: `tenormusica7@gmail.com`
- **パスワード**: `Tbbr43gb`

## 自動投稿手順

### 1. ログイン
```python
# ログインページにアクセス
playwright_navigate(url="https://note.com/login")

# メールアドレス入力
playwright_fill(
    selector='input[placeholder="mail@example.com or note ID"]',
    value="tenormusica@gmail.com"
)

# パスワード入力
playwright_fill(
    selector='input[type="password"]',
    value="Tbbr43gb"
)

# ログインボタンをクリック
playwright_click(selector='button:has-text("ログイン")')

# ページ遷移を待機
sleep 3
```

### 2. 新規投稿ページに移動
```python
# 投稿ボタンをクリック（座標クリック推奨）
playwright_click(selector='a[href="/notes/new"]')

# または直接URLにアクセス
playwright_navigate(url="https://note.com/notes/new")

# ページロードを待機
sleep 2
```

### 3. 記事の入力

#### タイトル入力
```python
# タイトルフィールドをクリック
playwright_click(selector='[contenteditable="true"]')

# タイトルを入力
playwright_fill(
    selector='[contenteditable="true"]',
    value="記事タイトル"
)

# 本文フィールドに移動するためEnterキー
playwright_press_key(key="Enter")
```

#### 本文入力
```python
# 本文を入力（タイトルを含まないセレクタを使用）
playwright_fill(
    selector='[contenteditable="true"]:not(:has-text("記事タイトル"))',
    value="記事本文の内容..."
)

# 入力完了を待機
sleep 2
```

### 4. 下書き保存
```python
# 下書き保存ボタンをクリック
playwright_click(selector='button:has-text("下書き保存")')

# 保存完了を待機
sleep 3

# スクリーンショットで確認
playwright_screenshot(name="note_draft_saved")
```

### 5. 投稿完了の確認
```python
# 下書き一覧ページにアクセス（メニューから）
# または直接URL: https://note.com/[username]/drafts

# スクリーンショットで下書き保存を確認
playwright_screenshot(name="note_drafts_list")
```

## 複数記事の投稿

### 記事ファイルの読み込み
```python
# Markdownファイルから記事を読み込む
with open("articles/article1.md", "r", encoding="utf-8") as f:
    content = f.read()

# タイトルと本文を分離
lines = content.strip().split("\n")
title = lines[0].replace("# ", "")  # 最初の行（# タイトル）
body = "\n".join(lines[1:]).strip()  # 残りの部分
```

### ループ処理
```python
articles = [
    "articles/article1.md",
    "articles/article2.md"
]

for article_path in articles:
    # 記事を読み込む
    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.strip().split("\n")
    title = lines[0].replace("# ", "")
    body = "\n".join(lines[1:]).strip()
    
    # 新規投稿ページに移動
    playwright_navigate(url="https://note.com/notes/new")
    sleep 2
    
    # タイトル入力
    playwright_fill(selector='[contenteditable="true"]', value=title)
    playwright_press_key(key="Enter")
    
    # 本文入力
    playwright_fill(
        selector=f'[contenteditable="true"]:not(:has-text("{title}"))',
        value=body
    )
    sleep 2
    
    # 下書き保存
    playwright_click(selector='button:has-text("下書き保存")')
    sleep 3
    
    print(f"✅ {title} - 下書き保存完了")
```

## 投稿ログの記録

### JSON形式でログ保存
```python
import json
from datetime import datetime

# ログファイルの読み込み（存在しない場合は新規作成）
log_file = "note_posted_articles.json"
if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        log_data = json.load(f)
else:
    log_data = {"posted": []}

# 新しい投稿を追加
log_data["posted"].append({
    "file": article_path,
    "note_id": "記事ID（URLから取得）",
    "note_url": "編集ページのURL",
    "title": title,
    "posted_at": datetime.now().isoformat(),
    "status": "draft"
})

# ログファイルに保存
with open(log_file, "w", encoding="utf-8") as f:
    json.dump(log_data, f, ensure_ascii=False, indent=2)
```

## 注意事項

### セレクタの安定性
- note.comのUIは変更される可能性があるため、セレクタが機能しない場合は座標クリックを使用
- 座標クリック例: `playwright_click(selector="button", x=1170, y=24)`

### 待機時間
- ページ遷移後は必ず `sleep()` で待機
- ネットワーク速度により待機時間を調整

### エラーハンドリング
- セレクタが見つからない場合のフォールバック処理
- スクリーンショットによる状態確認

### 既存記事の重複投稿防止
```python
# ログファイルから既投稿記事をチェック
posted_files = [entry["file"] for entry in log_data["posted"]]

for article_path in articles:
    if article_path in posted_files:
        print(f"⏭️ {article_path} - すでに投稿済みのためスキップ")
        continue
    
    # 投稿処理...
```

## トラブルシューティング

### ログインできない
- メールアドレス・パスワードが正しいか確認
- セッションが残っている場合はスキップ

### 投稿ボタンが見つからない
- URLを直接指定: `https://note.com/notes/new`
- ページのHTMLを確認: `playwright_evaluate(script="document.body.innerHTML")`

### 下書き保存されない
- 下書き保存ボタンのセレクタを確認
- 保存完了まで十分な待機時間を確保
- スクリーンショットで状態確認

## 参考資料
- note.com公式サイト: https://note.com/
- Playwright MCPドキュメント（Claude Code環境）
