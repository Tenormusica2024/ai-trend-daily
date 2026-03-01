import time
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

EMAIL = "tenormusica7@gmail.com"
PASSWORD = "Tbbr43gb"
ARTICLE = "articles/affine-notion-alternative-privacy-first-2025.md"

def read_article(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.strip().split("\n")
    title = lines[0].replace("# ", "")
    body = "\n".join(lines[1:]).strip()
    return title, body

def publish_to_note(title, body):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        print("[1/8] Login page...")
        page.goto("https://note.com/login")
        time.sleep(2)
        print("[2/8] Enter credentials...")
        page.fill('input[placeholder="mail@example.com or note ID"]', EMAIL)
        page.fill('input[type="password"]', PASSWORD)
        print("[3/8] Login...")
        page.click('button:has-text("ログイン")')
        time.sleep(3)
        print("[4/8] Navigate to new post...")
        page.goto("https://note.com/notes/new")
        time.sleep(2)
        print("[5/8] Click body editor...")
        page.click('[contenteditable="true"]')
        time.sleep(0.5)
        print("[6/8] Navigate to title with arrow up...")
        page.keyboard.press('ArrowUp')
        time.sleep(0.5)
        print("Enter title...")
        page.keyboard.type(title)
        time.sleep(1)
        print("Navigate back to body with arrow down...")
        page.keyboard.press('ArrowDown')
        time.sleep(0.5)
        print("Enter body...")
        page.keyboard.type(body)
        time.sleep(2)
        print("[7/8] Click publish button...")
        page.click('button:has-text("公開に進む")')
        time.sleep(3)
        print("[8/8] Add hashtags...")
        hashtag_input = page.locator('input[placeholder="ハッシュタグを追加する"]')
        hashtag_input.fill('AI')
        page.keyboard.press('Enter')
        time.sleep(0.5)
        hashtag_input.fill('Notion')
        page.keyboard.press('Enter')
        time.sleep(0.5)
        hashtag_input.fill('AFFiNE')
        page.keyboard.press('Enter')
        time.sleep(1)
        print("Click final publish button...")
        page.click('button:has-text("投稿する")')
        time.sleep(3)
        current_url = page.url
        print(f"OK: {current_url}")
        browser.close()
        return current_url

print(f"\nArticle: {ARTICLE}")
title, body = read_article(ARTICLE)
print(f"  Title: {title}")
print(f"  Body: {len(body)} chars")

try:
    note_url = publish_to_note(title, body)
    posted_log = {"file": ARTICLE, "title": title, "note_url": note_url, "posted_at": datetime.now().isoformat(), "status": "published"}
    
    log_file = "note_posted_articles.json"
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            log_data = json.load(f)
    else:
        log_data = {"posted": []}
    log_data["posted"].append(posted_log)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print("  SUCCESS - Article published")
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()
