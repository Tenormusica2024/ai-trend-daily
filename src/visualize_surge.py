"""
1週間急上昇ワード可視化モジュール
JSON/HTML形式で出力
"""
import json
from datetime import datetime
from calculate_weekly_surge import get_top_surge_keywords

def generate_surge_json():
    """
    急上昇ランキングをJSON形式で出力
    """
    surge_ranking = get_top_surge_keywords(20)
    
    if not surge_ranking:
        print("[WARNING] No surge ranking data available")
        return
    
    # JSON形式に変換
    output = {
        "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "analysis_type": "weekly_surge",
        "period": "Recent 3 days vs Past 7 days average",
        "ranking": []
    }
    
    for rank, data in enumerate(surge_ranking, 1):
        output["ranking"].append({
            "rank": rank,
            "keyword": data['keyword'],
            "surge_rate": round(data['surge_rate'], 1),
            "recent_avg": round(data['recent_avg'], 1),
            "baseline_avg": round(data['baseline_avg'], 1),
            "recent_views": data['recent_views']
        })
    
    # JSONファイルに保存
    with open('output/surge_ranking.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n[SUCCESS] JSON saved to output/surge_ranking.json")

def generate_surge_html():
    """
    急上昇ランキングをHTML形式で出力
    """
    surge_ranking = get_top_surge_keywords(20)
    
    if not surge_ranking:
        print("[WARNING] No ranking data available")
        return
    
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Trend Keywords - Weekly Surge Top 20</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        h1 {{
            color: #2d3748;
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .updated {{
            color: #718096;
            font-size: 0.9rem;
        }}
        
        .ranking {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .rank-item {{
            display: flex;
            align-items: center;
            padding: 1rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }}
        
        .rank-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .rank-number {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #667eea;
            min-width: 50px;
            text-align: center;
        }}
        
        .keyword {{
            flex: 1;
            font-size: 1.1rem;
            color: #2d3748;
            padding: 0 1rem;
        }}
        
        .surge-rate {{
            font-size: 1.3rem;
            font-weight: bold;
            min-width: 120px;
            text-align: right;
        }}
        
        .surge-rate.high {{
            color: #48bb78;  /* 緑 - 高い上昇率 */
        }}
        
        .surge-rate.medium {{
            color: #ed8936;  /* オレンジ - 中程度 */
        }}
        
        .surge-rate.low {{
            color: #f56565;  /* 赤 - 低い/マイナス */
        }}
        
        .views {{
            color: #718096;
            font-size: 0.9rem;
            min-width: 120px;
            text-align: right;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI Trend Keywords - Weekly Surge</h1>
            <p class="updated">Last Updated: {updated_at}</p>
            <p class="updated">直近3日 vs 過去7日平均比較</p>
        </div>
        
        <div class="ranking">
"""
    
    for rank, data in enumerate(surge_ranking, 1):
        surge_rate = data['surge_rate']
        
        # 上昇率に応じてクラス分け
        if surge_rate >= 50:
            rate_class = "high"
        elif surge_rate >= 0:
            rate_class = "medium"
        else:
            rate_class = "low"
        
        html += f"""            <div class="rank-item">
                <div class="rank-number">#{rank}</div>
                <div class="keyword">{data['keyword']}</div>
                <div class="surge-rate {rate_class}">{surge_rate:+.1f}%</div>
                <div class="views">{data['recent_views']:,} views</div>
            </div>
"""
    
    html += """        </div>
    </div>
</body>
</html>"""
    
    # HTMLファイルに保存
    with open('output/surge_ranking.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[SUCCESS] HTML saved to output/surge_ranking.html")

if __name__ == "__main__":
    print("Generating Weekly Surge Ranking...")
    generate_surge_json()
    generate_surge_html()
