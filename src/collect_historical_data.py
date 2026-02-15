"""
過去60日分のデータを一括収集
成長率分析に必要な履歴データを構築
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
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article}/daily/{date_str}/{date_str}"
        
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                return data['items'][0]['views']
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] {article} on {date.strftime('%Y-%m-%d')}: {e}")
        return 0

def collect_historical_data(days=60):
    """
    過去N日分のデータを収集
    
    Args:
        days: 収集する日数（デフォルト60日）
    """
    db = TrendDatabase()
    
    print("=" * 70)
    print(f"Historical Data Collection - Past {days} Days")
    print("=" * 70)
    print(f"Target Keywords: {len(AI_KEYWORDS)}")
    print(f"Date Range: {days} days back from today")
    print()
    
    total_requests = len(AI_KEYWORDS) * days
    completed = 0
    
    # 日付ごとにデータ収集
    for day_offset in range(1, days + 1):
        target_date = datetime.now() - timedelta(days=day_offset)
        date_str = target_date.strftime('%Y-%m-%d')
        
        print(f"\n[{day_offset}/{days}] Collecting data for {date_str}...")
        
        for i, keyword in enumerate(AI_KEYWORDS, 1):
            pageviews = get_pageviews_for_date(keyword, target_date)
            
            if pageviews > 0:
                # データベースに保存（日付を手動設定）
                collected_at = target_date.strftime('%Y-%m-%d %H:%M:%S')
                db.cursor.execute('''
                    INSERT INTO trends (keyword, pageviews, collected_at, rank)
                    VALUES (?, ?, ?, NULL)
                ''', (keyword, pageviews, collected_at))
                
                print(f"  [{i}/{len(AI_KEYWORDS)}] {keyword}: {pageviews:,} views")
            else:
                print(f"  [{i}/{len(AI_KEYWORDS)}] {keyword}: No data")
            
            completed += 1
            progress = (completed / total_requests) * 100
            print(f"  Progress: {completed}/{total_requests} ({progress:.1f}%)")
            
            # レート制限対策
            time.sleep(0.2)
        
        db.conn.commit()
    
    db.close()
    
    print()
    print("=" * 70)
    print("Historical Data Collection Completed")
    print("=" * 70)

if __name__ == "__main__":
    # 過去60日分のデータを収集
    collect_historical_data(60)
