"""
過去7日分のデータを収集
1週間急上昇ワード検出用
"""
import requests
from datetime import datetime, timedelta
import time
from config import AI_KEYWORDS, USER_AGENT
from database import TrendDatabase

def get_pageviews_for_date(article, date):
    """
    指定日のページビュー数を取得
    
    Args:
        article: Wikipedia記事名
        date: datetime オブジェクト
    
    Returns:
        int: ページビュー数
    """
    try:
        date_str = date.strftime('%Y%m%d')
        
        # 日本語版Wikipedia対応
        if '人工知能モデル' in article:
            url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/ja.wikipedia/all-access/all-agents/{article}/daily/{date_str}/{date_str}"
        else:
            url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article}/daily/{date_str}/{date_str}"
        
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                return data['items'][0]['views']
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] {article} on {date.strftime('%Y-%m-%d')}: {e}")
        return 0

def collect_week_data():
    """
    過去7日分のデータを収集
    """
    db = TrendDatabase()
    
    print("=" * 70)
    print("Weekly Data Collection - Past 7 Days")
    print("=" * 70)
    print(f"Target Keywords: {len(AI_KEYWORDS)}")
    print(f"Date Range: Past 7 days from today")
    print()
    
    # 過去7日分を収集
    for day_offset in range(1, 8):
        target_date = datetime.now() - timedelta(days=day_offset)
        date_str = target_date.strftime('%Y-%m-%d')
        
        print(f"\n[Day {day_offset}/7] Collecting data for {date_str}...")
        
        for i, keyword in enumerate(AI_KEYWORDS, 1):
            pageviews = get_pageviews_for_date(keyword, target_date)
            
            if pageviews > 0:
                # データベースに保存
                collected_at = target_date.strftime('%Y-%m-%d %H:%M:%S')
                db.cursor.execute('''
                    INSERT INTO trends (keyword, pageviews, collected_at, rank)
                    VALUES (?, ?, ?, NULL)
                ''', (keyword, pageviews, collected_at))
                
                print(f"  [{i}/{len(AI_KEYWORDS)}] {keyword}: {pageviews:,} views")
            else:
                print(f"  [{i}/{len(AI_KEYWORDS)}] {keyword}: No data")
            
            # レート制限対策
            time.sleep(0.1)
        
        db.conn.commit()
    
    db.close()
    
    print()
    print("=" * 70)
    print("Weekly Data Collection Completed")
    print("=" * 70)

if __name__ == "__main__":
    collect_week_data()
