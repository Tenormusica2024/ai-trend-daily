"""
note.com 完全自動投稿スクリプト（Playwright MCP版）
Claude Code環境でPlaywright MCPツールを使用
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

# note アカウント情報
NOTE_EMAIL = "tenormusica7@gmail.com"
NOTE_PASSWORD = "Tbbr43gb"
NOTE_CREATOR_NAME = "Urayaha Days"
NOTE_ID = "urayahadays"

# 記事保存ディレクトリ
ARTICLES_DIR = Path(__file__).parent / "articles"
POSTED_LOG = Path(__file__).parent / "note_posted_articles.json"


def load_posted_log():
    """投稿済み記事ログを読み込み"""
    if POSTED_LOG.exists():
        with open(POSTED_LOG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"posted": []}


def save_posted_log(posted_articles):
    """投稿済み記事ログを保存"""
    with open(POSTED_LOG, 'w', encoding='utf-8') as f:
        json.dump(posted_articles, f, indent=2, ensure_ascii=False)


def mark_as_posted(posted_articles, article_path: str, note_url: str):
    """記事を投稿済みとしてマーク"""
    posted_articles["posted"].append({
        "file": article_path,
        "note_url": note_url,
        "posted_at": datetime.now().isoformat()
    })
    save_posted_log(posted_articles)


def is_already_posted(posted_articles, article_path: str) -> bool:
    """記事が既に投稿済みか確認"""
    return any(item["file"] == article_path for item in posted_articles["posted"])


def get_unposted_articles(posted_articles):
    """未投稿の記事リストを取得"""
    unposted = []
    if not ARTICLES_DIR.exists():
        print(f"❌ 記事ディレクトリが存在しません: {ARTICLES_DIR}")
        return unposted
    
    for md_file in ARTICLES_DIR.glob("*.md"):
        if not is_already_posted(posted_articles, str(md_file)):
            unposted.append(md_file)
    
    return unposted


def read_article(article_path: Path):
    """記事ファイルを読み込み、タイトルと本文を抽出"""
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 最初の # で始まる行をタイトルとして抽出
    lines = content.split('\n')
    title = ""
    body_start_index = 0
    
    for i, line in enumerate(lines):
        if line.startswith('# '):
            title = line.replace('# ', '').strip()
            body_start_index = i + 1
            break
    
    # タイトル以降を本文として取得
    body = '\n'.join(lines[body_start_index:]).strip()
    
    return title, body


def post_to_note_playwright(article_path: Path):
    """
    Playwright MCPを使用してnoteに自動投稿
    
    このスクリプトはClaude Code環境で実行する想定
    以下のPlaywright MCPツールを使用：
    - mcp__playwright__playwright_navigate
    - mcp__playwright__playwright_fill
    - mcp__playwright__playwright_click
    - mcp__playwright__playwright_screenshot
    
    手順:
    1. note.comログインページにアクセス
    2. メールアドレス・パスワードを入力してログイン
    3. 「投稿」ボタンをクリック
    4. 「テキスト」を選択
    5. タイトルと本文を入力
    6. 「公開する」ボタンをクリック
    7. 公開されたURLを取得
    
    注意: 
    - このスクリプト単体では実行できません
    - Claude Codeセッション内でMCPツールを呼び出す必要があります
    - 実行例はREADME参照
    """
    title, body = read_article(article_path)
    
    print(f"\n📝 記事投稿準備")
    print(f"タイトル: {title}")
    print(f"本文文字数: {len(body)}文字")
    print(f"ファイル: {article_path.name}\n")
    
    print("⚠️ この関数はClaude Code環境でPlaywright MCPツールと共に実行する必要があります")
    print("手動実行の場合は note_auto_poster.py を使用してください\n")
    
    # Playwright MCP実行コマンド例を表示
    print("=" * 60)
    print("Claude Codeで実行するPlaywright MCPコマンド例:")
    print("=" * 60)
    print("""
# 1. noteログインページにアクセス
mcp__playwright__playwright_navigate(url="https://note.com/login")

# 2. メールアドレス入力
mcp__playwright__playwright_fill(selector="input[type='email']", value="tenormusica7@gmail.com")

# 3. パスワード入力
mcp__playwright__playwright_fill(selector="input[type='password']", value="Tbbr43gb")

# 4. ログインボタンクリック
mcp__playwright__playwright_click(selector="button[type='submit']")

# 5. 投稿ボタンをクリック（ログイン後）
sleep(3)  # ページ遷移待機
mcp__playwright__playwright_click(selector="a[href='/note/new']")

# 6. テキスト投稿を選択
mcp__playwright__playwright_click(selector="button:has-text('テキスト')")

# 7. タイトル入力
mcp__playwright__playwright_fill(selector="input[placeholder='タイトル']", value="{title}")

# 8. 本文入力
mcp__playwright__playwright_fill(selector="textarea[placeholder='本文']", value="{body[:1000]}...")

# 9. 公開ボタンクリック
mcp__playwright__playwright_click(selector="button:has-text('公開する')")

# 10. スクリーンショット撮影で確認
mcp__playwright__playwright_screenshot(name="note_posted")
""")
    print("=" * 60 + "\n")
    
    return None


def main():
    """メイン実行関数"""
    print("\n" + "="*60)
    print("🚀 note.com 自動投稿システム（Playwright版）")
    print("="*60 + "\n")
    
    posted_articles = load_posted_log()
    unposted = get_unposted_articles(posted_articles)
    
    if not unposted:
        print("✅ すべての記事が投稿済みです")
        return
    
    print(f"📄 未投稿の記事: {len(unposted)}件\n")
    
    for i, article in enumerate(unposted, 1):
        print(f"\n[{i}/{len(unposted)}] {article.name}")
        print("-"*60)
        
        post_to_note_playwright(article)
        
        print("\n⚠️ Playwright MCPツールを使用して投稿を完了してください")
        print("投稿完了後、URLを入力してログに記録できます\n")
        
        # 投稿完了確認
        note_url = input("投稿完了後、note記事のURLを入力してください（スキップする場合はEnter）: ").strip()
        
        if note_url:
            mark_as_posted(posted_articles, str(article), note_url)
            print(f"✅ 投稿記録を保存しました: {note_url}")
        else:
            print("⚠️ 投稿記録をスキップしました")
        
        # 次の記事に進むか確認
        if i < len(unposted):
            continue_input = input("\n次の記事に進みますか？ (y/n): ").strip().lower()
            if continue_input != 'y':
                print("\n⏸️  投稿を中断しました")
                break
    
    print("\n" + "="*60)
    print("✅ 処理完了")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
