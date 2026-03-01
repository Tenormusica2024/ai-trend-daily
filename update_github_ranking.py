#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trend Ranking Updater
GitHubのトレンドリポジトリを取得してJSONファイルに保存
"""

import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time
def translate_to_japanese(text, retry_count=0, max_retries=3):
    """
    Gemini APIを使用して英語テキストを日本語に翻訳
    リトライ機能付き
    """
    if text == "No description provided":
        return "説明なし"
    
    # 短い固有名詞や技術用語は翻訳しない
    if len(text.split()) <= 3 and text[0].isupper():
        # 例: "OpenTelemetry Collector" のような固有名詞はそのまま
        pass
    
    API_KEY = "AIzaSyBKVL0MW3hbTFX7llfbuF0TL73SKNR2Rfw"
    # Gemini 2.0 Flash (thinking機能なし、安定版)
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
    
    prompt = f"""以下の英語のGitHubリポジトリ説明文を自然な日本語に翻訳してください。

【翻訳ルール】
1. 技術用語は適切に日本語化してください
2. 読みやすく簡潔な表現にしてください
3. 翻訳結果のみを出力し、説明や前置きは不要です
4. 原文の意味を正確に伝えてください

【原文】
{text}

【翻訳】"""
    
    try:
        response = requests.post(
            f"{API_URL}?key={API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.3,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 200,
                    "responseModalities": ["TEXT"]
                }
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            # レスポンス構造のデバッグ
            if 'candidates' in data and len(data['candidates']) > 0:
                candidate = data['candidates'][0]
                if 'content' in candidate:
                    content = candidate['content']
                    if 'parts' in content and len(content['parts']) > 0:
                        translated = content['parts'][0]['text'].strip()
                        # 翻訳結果が空または元のテキストと同じ場合はリトライ
                        if translated and translated != text:
                            return translated
                    elif 'text' in content:
                        # 新しいレスポンス形式の可能性
                        translated = content['text'].strip()
                        if translated and translated != text:
                            return translated
            # リトライ処理
            if retry_count < max_retries:
                print(f"Translation retry {retry_count + 1}/{max_retries} for: {text[:50]}...")
                time.sleep(1)  # リトライ前に待機
                return translate_to_japanese(text, retry_count + 1, max_retries)
            # 最終的なフォールバック
            print(f"Translation failed after {max_retries} retries: {text[:50]}...")
            return text
        else:
            # APIエラー時もリトライ
            if retry_count < max_retries:
                print(f"API error (status {response.status_code}), retry {retry_count + 1}/{max_retries}")
                time.sleep(2)  # エラー時はより長く待機
                return translate_to_japanese(text, retry_count + 1, max_retries)
            print(f"Translation API error after {max_retries} retries: {response.status_code}")
            return text
            
    except Exception as e:
        # 例外発生時もリトライ
        if retry_count < max_retries:
            print(f"Translation exception, retry {retry_count + 1}/{max_retries}: {str(e)}")
            time.sleep(2)
            return translate_to_japanese(text, retry_count + 1, max_retries)
        print(f"Translation error after {max_retries} retries: {e}")
        return text

def fetch_github_trending():
    """
    GitHubのトレンドページからトレンドリポジトリ情報を取得
    """
    url = "https://github.com/trending"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching GitHub trending: {e}")
        return None

def fetch_readme_summary(repo_name, max_length=500):
    """
    GitHub APIを使用してREADMEの概要を取得
    """
    api_url = f"https://api.github.com/repos/{repo_name}/readme"
    headers = {
        'Accept': 'application/vnd.github.v3.raw',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            readme_text = response.text
            # Markdown記号を削除してプレーンテキスト化
            import re
            # ヘッダー記号除去
            readme_text = re.sub(r'#+\s', '', readme_text)
            # リンク記号除去
            readme_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', readme_text)
            # コードブロック除去
            readme_text = re.sub(r'```[\s\S]*?```', '', readme_text)
            # インラインコード除去
            readme_text = re.sub(r'`([^`]+)`', r'\1', readme_text)
            # 改行を空白に変換
            readme_text = ' '.join(readme_text.split())
            # 最初の文章を取得（ピリオド区切り）
            sentences = readme_text.split('. ')
            summary = '. '.join(sentences[:3])  # 最初の3文を取得
            if len(summary) > max_length:
                summary = summary[:max_length] + '...'
            return summary if summary else None
        return None
    except Exception as e:
        print(f"Error fetching README for {repo_name}: {e}")
        return None

def parse_trending_repos(html_content):
    """
    HTMLからトレンドリポジトリ情報をパース
    """
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    repos = []
    
    # トレンドリポジトリのarticle要素を探す
    articles = soup.find_all('article', class_='Box-row')
    
    for idx, article in enumerate(articles[:20], 1):  # 上位20件を取得
        try:
            # リポジトリ名
            h2 = article.find('h2', class_='h3')
            if not h2:
                continue
            
            repo_link = h2.find('a')
            if not repo_link:
                continue
            
            repo_name = repo_link.get('href', '').strip('/')
            
            # 説明文
            desc_elem = article.find('p', class_='col-9')
            description = desc_elem.get_text(strip=True) if desc_elem else "No description provided"
            
            # プログラミング言語
            lang_elem = article.find('span', itemprop='programmingLanguage')
            language = lang_elem.get_text(strip=True) if lang_elem else ""
            
            # スター数取得（"1,289 stars today" 形式）
            stars = 0
            star_count = article.find('span', class_='d-inline-block float-sm-right')
            if star_count:
                stars_text = star_count.get_text(strip=True)
                try:
                    # "1,289 stars today" から数字のみ抽出
                    import re
                    numbers = re.findall(r'[\d,]+', stars_text)
                    if numbers:
                        stars = int(numbers[0].replace(',', ''))
                except:
                    pass
            
            # READMEの概要を取得
            print(f"Fetching README for {repo_name}...")
            readme_summary = fetch_readme_summary(repo_name)
            time.sleep(0.5)  # API制限回避
            
            # 説明文を日本語に翻訳（レート制限対策で1秒待機）
            description_ja = translate_to_japanese(description) if description != "No description provided" else "説明なし"
            time.sleep(1)  # API制限回避のため待機時間を延長
            
            # README概要も翻訳
            readme_summary_ja = None
            if readme_summary:
                readme_summary_ja = translate_to_japanese(readme_summary)
                time.sleep(1)
            
            repos.append({
                'rank': idx,
                'repo_name': repo_name,
                'description': description,
                'description_ja': description_ja,
                'readme_summary': readme_summary,
                'readme_summary_ja': readme_summary_ja,
                'language': language,
                'stars': stars
            })
            
        except Exception as e:
            print(f"Error parsing repo {idx}: {e}")
            continue
    
    return repos

def create_ranking_json(repos):
    """
    ランキングJSONファイルを作成
    """
    ranking_data = {
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_repos': len(repos),
        'ranking': repos
    }
    
    return ranking_data

def save_json(data, filepath):
    """
    JSONファイルを保存
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # Windows console output encoding issue workaround
        try:
            print("Saved: {}".format(filepath))
        except:
            print("Saved successfully")
        return True
    except Exception as e:
        print("Error saving JSON: {}".format(str(e)))
        return False

def main():
    """
    メイン処理
    """
    print("=" * 60)
    print("GitHub Trend Ranking Updater")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # GitHubトレンドページを取得
    print("\n[1/3] Fetching GitHub trending page...")
    html_content = fetch_github_trending()
    
    if not html_content:
        print("Failed to fetch GitHub trending page")
        return False
    
    # HTMLをパース
    print("[2/3] Parsing repository data...")
    repos = parse_trending_repos(html_content)
    
    if not repos:
        print("No repositories found")
        return False
    
    print(f"Found {len(repos)} trending repositories")
    
    # JSONファイルを作成
    print("[3/3] Creating JSON file...")
    ranking_data = create_ranking_json(repos)
    
    # JSONファイルを保存
    success = save_json(ranking_data, 'github_ranking.json')
    
    if success:
        print("\n" + "=" * 60)
        print("GitHub Trend Ranking Update Complete!")
        print("=" * 60)
        print("Updated at: {}".format(ranking_data['updated_at']))
        print("Total repositories: {}".format(ranking_data['total_repos']))
        print("\nTop 5 Repositories:")
        for repo in repos[:5]:
            try:
                print("  #{} {} ({} stars)".format(repo['rank'], repo['repo_name'], repo['stars']))
            except:
                print("  Repository: {}".format(repo['repo_name']))
    
    return success

if __name__ == '__main__':
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        exit(1)
    except Exception as e:
        print("\nUnexpected error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        exit(1)
