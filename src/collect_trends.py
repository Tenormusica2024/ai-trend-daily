"""
Wikipedia Pageviews APIからトレンドデータを収集
"""
import requests
from datetime import datetime, timedelta
import time
from config import AI_KEYWORDS, EXCLUDED_KEYWORDS, USER_AGENT
from database import TrendDatabase

def get_pageviews(article, days=1):
    """
    Wikipedia Pageviews APIから指定記事のページビュー数を取得
    
    Args:
        article: Wikipedia記事名
        days: 取得する日数（デフォルト: 1日前）
    
    Returns:
        int: ページビュー数
    """
    try:
        # 日付設定（昨日のデータを取得）
        end_date = datetime.now() - timedelta(days=days)
        start_date = end_date
        
        # API URL構築
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article}/daily/{start_date.strftime('%Y%m%d')}/{end_date.strftime('%Y%m%d')}"
        
        headers = {
            'User-Agent': USER_AGENT
        }
        
        response = requests.get(url, headers=headers, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                return data['items'][0]['views']
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] {article}: {e}")
        return 0

def collect_all_trends():
    """全キーワードのトレンドデータを収集してTop10を抽出"""
    print("=" * 70)
    print("AI Trend Keywords Collection - Wikipedia Pageviews API")
    print("=" * 70)
    print(f"Target Keywords: {len(AI_KEYWORDS)}")
    print(f"Collection Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # データ収集
    trends = []
    
    for i, keyword in enumerate(AI_KEYWORDS, 1):
        print(f"[{i}/{len(AI_KEYWORDS)}] {keyword}...", end=" ", flush=True)
        
        pageviews = get_pageviews(keyword)
        
        if pageviews > 0:
            trends.append({
                'keyword': keyword,
                'pageviews': pageviews
            })
            print(f"{pageviews:,} views")
        else:
            print("No data")
        
        # レート制限対策（100ms待機 - 高速化）
        time.sleep(0.1)
    
    # 除外ワードをフィルタリング
    filtered_trends = [t for t in trends if t['keyword'] not in EXCLUDED_KEYWORDS]
    
    # Top20抽出
    filtered_trends.sort(key=lambda x: x['pageviews'], reverse=True)
    top10 = filtered_trends[:20]
    
    print()
    print("=" * 70)
    print("Top 20 AI Trend Keywords")
    print("=" * 70)
    
    # データベースに保存
    db = TrendDatabase()
    
    for rank, trend in enumerate(top10, 1):
        keyword = trend['keyword']
        pageviews = trend['pageviews']
        
        print(f"#{rank:2d} {keyword:40s} {pageviews:>10,} views")
        
        # データベースに挿入
        db.insert_trend(keyword, pageviews, rank)
    
    # 古いデータのクリーンアップ
    deleted = db.cleanup_old_data()
    if deleted > 0:
        print(f"\n[INFO] Cleaned up {deleted} old records")
    
    db.close()
    
    print()
    print("=" * 70)
    print("Collection Completed")
    print("=" * 70)
    
    return top10

if __name__ == "__main__":
    collect_all_trends()
