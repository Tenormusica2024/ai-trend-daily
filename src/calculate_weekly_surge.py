"""
1週間急上昇ワード検出モジュール
直近3日平均 vs 過去7日平均の比較で急上昇を検出
"""
from datetime import datetime, timedelta
from database import TrendDatabase
from config import AI_KEYWORDS, EXCLUDED_KEYWORDS

def calculate_weekly_surge(keyword, db):
    """
    1週間の急上昇率を計算
    
    Args:
        keyword: Wikipedia記事名
        db: TrendDatabase インスタンス
    
    Returns:
        dict: {
            'keyword': str,
            'recent_avg': float (直近3日平均),
            'baseline_avg': float (過去7日平均),
            'surge_rate': float (急上昇率 %),
            'recent_views': int
        }
        データ不足の場合は None
    """
    # 過去7日のデータ取得
    week_data = db.get_keyword_history(keyword, days=7)
    
    # データ不足チェック（最低5日分必要）
    if len(week_data) < 5:
        return None
    
    # 直近3日の平均（最新データから3件）
    recent_data = week_data[:3]
    recent_views = [row[1] for row in recent_data]
    recent_avg = sum(recent_views) / len(recent_views)
    
    # 過去7日の平均（全データ）
    all_views = [row[1] for row in week_data]
    baseline_avg = sum(all_views) / len(all_views)
    
    # 急上昇率計算
    if baseline_avg == 0:
        return None
    
    surge_rate = ((recent_avg - baseline_avg) / baseline_avg) * 100
    
    return {
        'keyword': keyword,
        'recent_avg': recent_avg,
        'baseline_avg': baseline_avg,
        'surge_rate': surge_rate,
        'recent_views': int(recent_avg)
    }

def get_top_surge_keywords(limit=20):
    """
    1週間急上昇Top20のキーワードを取得
    
    Returns:
        list: 急上昇率順のキーワードリスト
    """
    db = TrendDatabase()
    
    surge_data = []
    
    print("=" * 70)
    print("Weekly Surge Analysis - AI Trend Keywords")
    print("=" * 70)
    print(f"Analysis: Recent 3 days vs Past 7 days average")
    print(f"Target Keywords: {len(AI_KEYWORDS)}")
    print()
    
    for i, keyword in enumerate(AI_KEYWORDS, 1):
        print(f"[{i}/{len(AI_KEYWORDS)}] {keyword}...", end=" ", flush=True)
        
        result = calculate_weekly_surge(keyword, db)
        
        if result:
            surge_data.append(result)
            print(f"{result['surge_rate']:+.1f}% (Recent: {result['recent_views']:,} views)")
        else:
            print("Insufficient data")
    
    db.close()
    
    # 除外ワードフィルタリング
    filtered_surge = [s for s in surge_data if s['keyword'] not in EXCLUDED_KEYWORDS]
    
    # 急上昇率でソート
    filtered_surge.sort(key=lambda x: x['surge_rate'], reverse=True)
    
    # Top20抽出
    top20 = filtered_surge[:limit]
    
    print()
    print("=" * 70)
    print(f"Top {limit} Surging AI Keywords (Weekly - Excluding Common Words)")
    print("=" * 70)
    
    for rank, data in enumerate(top20, 1):
        print(f"#{rank:2d} {data['keyword']:40s} {data['surge_rate']:+7.1f}% "
              f"({data['recent_views']:,} views)")
    
    print()
    print("=" * 70)
    print("Analysis Completed")
    print("=" * 70)
    
    return top20

if __name__ == "__main__":
    get_top_surge_keywords(20)
