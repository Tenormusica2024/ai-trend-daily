"""
成長率ランキング可視化モジュール
JSON/HTML形式で成長率ランキングを出力
"""
import json
import os
from datetime import datetime
from calculate_growth import get_top_growth_keywords
from config import OUTPUT_JSON, OUTPUT_HTML

def generate_growth_json():
    """成長率ランキングをJSON形式で出力"""
    # 成長率データ取得
    growth_ranking = get_top_growth_keywords(10)
    
    if not growth_ranking:
        print("[WARNING] No ranking data available")
        return None
    
    # JSON構造作成
    data = {
        "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "analysis_type": "growth_rate",
        "period": "Recent 7 days vs Past 60 days average",
        "ranking": []
    }
    
    for rank, item in enumerate(growth_ranking, 1):
        data["ranking"].append({
            "rank": rank,
            "keyword": item['keyword'].replace("_", " "),
            "growth_rate": round(item['growth_rate'], 1),
            "recent_avg": int(item['recent_avg']),
            "baseline_avg": int(item['baseline_avg'])
        })
    
    # outputディレクトリ作成
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    
    # JSON保存
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] JSON saved: {OUTPUT_JSON}")
    
    return data

def generate_growth_html():
    """成長率ランキングをHTML形式で出力"""
    # 成長率データ取得
    growth_ranking = get_top_growth_keywords(10)
    
    if not growth_ranking:
        print("[WARNING] No ranking data available")
        return
    
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Trend Keywords Top 10 (Growth Rate)</title>
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
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .updated {{
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.9rem;
        }}
        
        .ranking {{
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}
        
        .rank-item {{
            display: flex;
            align-items: center;
            padding: 1rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 12px;
            transition: transform 0.2s;
        }}
        
        .rank-item:hover {{
            transform: translateX(10px);
        }}
        
        .rank-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            min-width: 60px;
        }}
        
        .rank-number.top3 {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .keyword {{
            flex: 1;
            font-size: 1.1rem;
            font-weight: 600;
            color: #2d3748;
        }}
        
        .views-info {{
            font-size: 0.85rem;
            color: #64748b;
            margin-top: 0.25rem;
            font-weight: 400;
        }}
        
        .growth-rate {{
            font-size: 1.3rem;
            font-weight: bold;
            min-width: 120px;
            text-align: right;
        }}
        
        .growth-rate.positive {{
            color: #10b981;
        }}
        
        .growth-rate.negative {{
            color: #ef4444;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 AI Trend Keywords - Growth Rate</h1>
            <p class="updated">Last Updated: {updated_at}</p>
            <p class="updated" style="font-size: 0.85rem; margin-top: 0.5rem;">直近7日 vs 過去60日平均比較</p>
        </div>
        
        <div class="ranking">
"""
    
    for rank, item in enumerate(growth_ranking, 1):
        keyword_display = item['keyword'].replace("_", " ")
        top3_class = " top3" if rank <= 3 else ""
        growth_rate = item['growth_rate']
        growth_class = "positive" if growth_rate > 0 else "negative"
        growth_sign = "+" if growth_rate > 0 else ""
        
        html += f"""            <div class="rank-item">
                <div class="rank-number{top3_class}">#{rank}</div>
                <div class="keyword">
                    {keyword_display}
                    <div class="views-info">{item['recent_avg']:,.0f} views (直近7日平均)</div>
                </div>
                <div class="growth-rate {growth_class}">{growth_sign}{growth_rate:.1f}%</div>
            </div>
"""
    
    html += """        </div>
    </div>
</body>
</html>"""
    
    # outputディレクトリ作成
    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    
    # HTML保存
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[OK] HTML saved: {OUTPUT_HTML}")

if __name__ == "__main__":
    print("=" * 70)
    print("Generate Growth Rate Ranking Visualization")
    print("=" * 70)
    
    generate_growth_json()
    generate_growth_html()
    
    print()
    print("=" * 70)
    print("Visualization Completed")
    print("=" * 70)
