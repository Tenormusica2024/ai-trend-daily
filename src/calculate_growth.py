"""
伸び率計算モジュール
直近7日平均と過去60日平均を比較して成長率を算出
"""
from datetime import datetime, timedelta
from database import TrendDatabase
from config import AI_KEYWORDS, EXCLUDED_KEYWORDS

def calculate_growth_rate(keyword, db):
    """
    キーワードの成長率を計算
    
    Args:
        keyword: Wikipedia記事名
        db: TrendDatabase インスタンス
    
    Returns:
        dict: {
            'keyword': str,
            'recent_avg': float (直近7日平均),
            'baseline_avg': float (過去60日平均),
            'growth_rate': float (成長率 %)
        }
        データ不足の場合は None
    """
    # 直近7日のデータ取得
    recent_data = db.get_keyword_history(keyword, days=7)
    
    # 過去60日のデータ取得
    all_data = db.get_keyword_history(keyword, days=60)
    
    # データ不足チェック
    if len(recent_data) < 3 or len(all_data) < 30:
        return None
    
    # 直近7日の平均
    recent_views = [row[1] for row in recent_data]
    recent_avg = sum(recent_views) / len(recent_views)
    
    # 過去60日のデータから直近7日を除外してベースライン計算
    baseline_data = all_data[7:]  # 直近7日を除外
    if len(baseline_data) < 20:
        return None
    
    baseline_views = [row[1] for row in baseline_data]
    baseline_avg = sum(baseline_views) / len(baseline_views)
    
    # 成長率計算（ベースラインがゼロの場合は計算不可）
    if baseline_avg == 0:
        return None
    
    growth_rate = ((recent_avg - baseline_avg) / baseline_avg) * 100
    
    return {
        'keyword': keyword,
        'recent_avg': recent_avg,
        'baseline_avg': baseline_avg,
        'growth_rate': growth_rate,
        'recent_views': int(recent_avg)
    }

def get_top_growth_keywords(limit=10):
    """
    成長率Top10のキーワードを取得
    
    Returns:
        list: 成長率順のキーワードリスト
    """
    db = TrendDatabase()
    
    growth_data = []
    
    print("=" * 70)
    print("AI Keywords Growth Rate Analysis")
    print("=" * 70)
    print(f"Analysis Period: Recent 7 days vs Past 60 days average")
    print(f"Target Keywords: {len(AI_KEYWORDS)}")
    print()
    
    for i, keyword in enumerate(AI_KEYWORDS, 1):
        print(f"[{i}/{len(AI_KEYWORDS)}] {keyword}...", end=" ", flush=True)
        
        result = calculate_growth_rate(keyword, db)
        
        if result:
            growth_data.append(result)
            print(f"{result['growth_rate']:+.1f}% (Recent: {result['recent_views']:,} views)")
        else:
            print("Insufficient data")
    
    db.close()
    
    # 成長率でソート
    growth_data.sort(key=lambda x: x['growth_rate'], reverse=True)
    
    # Top10抽出
    top10 = growth_data[:limit]
    
    print()
    print("=" * 70)
    print(f"Top {limit} Growing AI Keywords (7-day vs 60-day average)")
    print("=" * 70)
    
    for rank, data in enumerate(top10, 1):
        print(f"#{rank:2d} {data['keyword']:40s} {data['growth_rate']:+7.1f}% "
              f"({data['recent_views']:,} views)")
    
    print()
    print("=" * 70)
    print("Analysis Completed")
    print("=" * 70)
    
    return top10

if __name__ == "__main__":
    get_top_growth_keywords(10)
