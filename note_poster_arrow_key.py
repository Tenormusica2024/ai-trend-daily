import time
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

EMAIL = "tenormusica7@gmail.com"
PASSWORD = "Tbbr43gb"
ARTICLES = ["articles/coinbase-x402-protocol-analysis-2025.md", "articles/affine-notion-alternative-privacy-first-2025.md"]

def read_article(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.strip().split("\n")
    title = lines[0].replace("# ", "")
    body = "\n".join(lines[1:]).strip()
    return title, body

def post_to_note(title, body):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        print("[1/7] Login page...")
        page.goto("https://note.com/login")
        time.sleep(2)
        print("[2/7] Enter credentials...")
        page.fill('input[placeholder="mail@example.com or note ID"]', EMAIL)
        page.fill('input[type="password"]', PASSWORD)
        print("[3/7] Login...")
        page.click('button:has-text("ログイン")')
        time.sleep(3)
        print("[4/7] Navigate to new post...")
        page.goto("https://note.com/notes/new")
        time.sleep(2)
        print("[5/7] Click body editor...")
        page.click('[contenteditable="true"]')
        time.sleep(0.5)
        print("[6/7] Navigate to title with arrow up...")
        page.keyboard.press('ArrowUp')
        time.sleep(0.5)
        print("[7/7] Enter title...")
        page.keyboard.type(title)
        time.sleep(1)
        print("Navigate back to body with arrow down...")
        page.keyboard.press('ArrowDown')
        time.sleep(0.5)
        print("Enter body...")
        page.keyboard.type(body)
        time.sleep(2)
        print("Save draft...")
        page.click('button:has-text("下書き保存")')
        time.sleep(3)
        current_url = page.url
        print(f"OK: {current_url}")
        browser.close()
        return current_url

posted_log = []
for article_path in ARTICLES:
    print(f"\nArticle: {article_path}")
    title, body = read_article(article_path)
    print(f"  Title: {title}")
    print(f"  Body: {len(body)} chars")
    try:
        note_url = post_to_note(title, body)
        posted_log.append({"file": article_path, "title": title, "note_url": note_url, "posted_at": datetime.now().isoformat(), "status": "draft"})
        print("  SUCCESS")
    except Exception as e:
        print(f"  ERROR: {e}")
        continue
    time.sleep(2)

log_file = "note_posted_articles.json"
if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        log_data = json.load(f)
else:
    log_data = {"posted": []}
log_data["posted"].extend(posted_log)
with open(log_file, "w", encoding="utf-8") as f:
    json.dump(log_data, f, ensure_ascii=False, indent=2)
print(f"\nCompleted: {len(posted_log)} articles posted")
