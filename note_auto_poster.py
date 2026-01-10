"""
note.com 自動投稿スクリプト
Playwright MCPを使用してnoteに記事を自動投稿
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

# note アカウント情報
NOTE_EMAIL = "tenormusica7@gmail.com"
NOTE_PASSWORD = os.getenv("NOTE_PASSWORD", "Tbbr43gb")  # 環境変数から取得（フォールバック含む）
NOTE_CREATOR_NAME = "Urayaha Days"
NOTE_ID = "urayahadays"

# 記事保存ディレクトリ
ARTICLES_DIR = Path(__file__).parent / "articles"
POSTED_LOG = Path(__file__).parent / "note_posted_articles.json"


class NoteAutoPoster:
    """note.com自動投稿クラス"""
    
    def __init__(self):
        self.posted_articles = self._load_posted_log()
    
    def _load_posted_log(self):
        """投稿済み記事ログを読み込み"""
        if POSTED_LOG.exists():
            with open(POSTED_LOG, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"posted": []}
    
    def _save_posted_log(self):
        """投稿済み記事ログを保存"""
        with open(POSTED_LOG, 'w', encoding='utf-8') as f:
            json.dump(self.posted_articles, f, indent=2, ensure_ascii=False)
    
    def _mark_as_posted(self, article_path: str, note_url: str):
        """記事を投稿済みとしてマーク"""
        self.posted_articles["posted"].append({
            "file": article_path,
            "note_url": note_url,
            "posted_at": datetime.now().isoformat()
        })
        self._save_posted_log()
    
    def _is_already_posted(self, article_path: str) -> bool:
        """記事が既に投稿済みか確認"""
        return any(item["file"] == article_path for item in self.posted_articles["posted"])
    
    def get_unposted_articles(self):
        """未投稿の記事リストを取得"""
        unposted = []
        if not ARTICLES_DIR.exists():
            print(f"❌ 記事ディレクトリが存在しません: {ARTICLES_DIR}")
            return unposted
        
        for md_file in ARTICLES_DIR.glob("*.md"):
            if not self._is_already_posted(str(md_file)):
                unposted.append(md_file)
        
        return unposted
    
    def read_article(self, article_path: Path):
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
    
    def post_to_note_manual_instructions(self, article_path: Path):
        """
        note投稿手順を表示（手動投稿用）
        完全自動化が難しい場合のフォールバック
        """
        title, body = self.read_article(article_path)
        
        print("\n" + "="*60)
        print("📝 note投稿手順（手動）")
        print("="*60)
        print(f"\n記事ファイル: {article_path.name}")
        print(f"タイトル: {title}\n")
        print("【手順】")
        print("1. https://note.com/login にアクセス")
        print(f"2. メールアドレス: {NOTE_EMAIL}")
        print(f"3. パスワード: {NOTE_PASSWORD}")
        print("4. ログイン後、「投稿」ボタンをクリック")
        print("5. 「テキスト」を選択")
        print(f"6. タイトルに以下を入力:\n   {title}")
        print(f"\n7. 本文に以下の内容を貼り付け:\n")
        print("-"*60)
        print(body[:500] + "..." if len(body) > 500 else body)
        print("-"*60)
        print("\n8. 必要に応じて画像を追加")
        print("9. 「公開設定」を確認（デフォルト: 全体公開）")
        print("10. 「公開する」ボタンをクリック")
        print("\n投稿完了後、URLをコピーしてください。")
        print("="*60 + "\n")
        
        # ユーザー入力待ち
        note_url = input("投稿完了後、note記事のURLを入力してください（スキップする場合はEnter）: ").strip()
        
        if note_url:
            self._mark_as_posted(str(article_path), note_url)
            print(f"✅ 投稿記録を保存しました: {note_url}")
        else:
            print("⚠️ 投稿記録をスキップしました")
        
        return note_url if note_url else None


def main():
    """メイン実行関数"""
    print("\n" + "="*60)
    print("🚀 note.com 自動投稿システム")
    print("="*60 + "\n")
    
    poster = NoteAutoPoster()
    unposted = poster.get_unposted_articles()
    
    if not unposted:
        print("✅ すべての記事が投稿済みです")
        return
    
    print(f"📄 未投稿の記事: {len(unposted)}件\n")
    
    for i, article in enumerate(unposted, 1):
        print(f"\n[{i}/{len(unposted)}] {article.name}")
        print("-"*60)
        
        # 現時点では手動投稿手順を表示
        # TODO: Playwright MCP統合による完全自動化
        poster.post_to_note_manual_instructions(article)
        
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
