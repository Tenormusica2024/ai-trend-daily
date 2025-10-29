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
def translate_to_japanese(text):
    """
    英語テキストを日本語に翻訳（簡易的な技術用語翻訳）
    """
    if text == "No description provided":
        return "説明なし"
    
    # 基本的な技術用語の翻訳マッピング
    translation_map = {
        "knowledge base": "ナレッジベース",
        "open-source": "オープンソース",
        "open source": "オープンソース",
        "self-hosted": "セルフホスト型",
        "implementation": "実装",
        "cross-platform": "クロスプラットフォーム",
        "desktop application": "デスクトップアプリケーション",
        "speech-to-text": "音声テキスト変換",
        "Machine Learning": "機械学習",
        "AI agent": "AIエージェント",
        "social media": "ソーシャルメディア",
        "free courses": "無料コース",
        "certifications": "認定資格",
        "payments protocol": "決済プロトコル",
        "tutorials": "チュートリアル",
        "real-world": "実世界の",
        "privacy first": "プライバシー優先",
        "customizable": "カスタマイズ可能",
        "planning": "計画",
        "sorting": "整理",
        "creating": "作成",
    }
    
    # 翻訳を適用（大文字小文字を無視）
    translated = text
    for eng, jpn in translation_map.items():
        # 大文字小文字を保持しつつ置換
        import re
        pattern = re.compile(re.escape(eng), re.IGNORECASE)
        translated = pattern.sub(jpn, translated)
    
    return translated

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
            
            # スター数（複数の取得方法を試行）
            stars = 0
            
            # 方法1: octicon-star から取得
            star_elem = article.find('svg', class_='octicon-star')
            if star_elem:
                parent = star_elem.find_parent('a')
                if parent:
                    stars_text = parent.get_text(strip=True)
                    try:
                        # "k" を 1000 に変換
                        if 'k' in stars_text.lower():
                            stars = int(float(stars_text.lower().replace('k', '').replace(',', '').strip()) * 1000)
                        else:
                            stars = int(stars_text.replace(',', '').strip())
                    except:
                        pass
            
            # 方法2: star-count クラスから取得
            if stars == 0:
                star_count = article.find('span', class_='d-inline-block float-sm-right')
                if star_count:
                    stars_text = star_count.get_text(strip=True)
                    try:
                        if 'k' in stars_text.lower():
                            stars = int(float(stars_text.lower().replace('k', '').replace(',', '').strip()) * 1000)
                        else:
                            stars = int(stars_text.replace(',', '').strip())
                    except:
                        pass
            
            # 説明文を日本語に翻訳
            description_ja = translate_to_japanese(description) if description != "No description provided" else "説明なし"
            
            repos.append({
                'rank': idx,
                'repo_name': repo_name,
                'description': description,
                'description_ja': description_ja,
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
