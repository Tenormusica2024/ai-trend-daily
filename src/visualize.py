"""
ランキング可視化モジュール
JSON/HTML形式でランキングを出力
"""
import json
import os
from datetime import datetime
from database import TrendDatabase
from config import OUTPUT_JSON, OUTPUT_HTML

def generate_json():
    """最新ランキングをJSON形式で出力"""
    db = TrendDatabase()
    ranking = db.get_latest_ranking(10)
    db.close()
    
    if not ranking:
        print("[WARNING] No ranking data available")
        return None
    
    # JSON構造作成
    data = {
        "updated_at": ranking[0][2] if ranking else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "ranking": []
    }
    
    for keyword, pageviews, collected_at, rank in ranking:
        data["ranking"].append({
            "rank": rank,
            "keyword": keyword.replace("_", " "),
            "pageviews": pageviews
        })
    
    # outputディレクトリ作成
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    
    # JSON保存
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] JSON saved: {OUTPUT_JSON}")
    
    return data

def generate_html():
    """最新ランキングをHTML形式で出力"""
    db = TrendDatabase()
    ranking = db.get_latest_ranking(10)
    db.close()
    
    if not ranking:
        print("[WARNING] No ranking data available")
        return
    
    updated_at = ranking[0][2] if ranking else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Trend Keywords Top 10</title>
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
            max-width: 800px;
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
        
        .pageviews {{
            font-size: 1rem;
            color: #667eea;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Trend Keywords</h1>
            <p class="updated">Last Updated: {updated_at}</p>
        </div>
        
        <div class="ranking">
"""
    
    for keyword, pageviews, collected_at, rank in ranking:
        keyword_display = keyword.replace("_", " ")
        top3_class = " top3" if rank <= 3 else ""
        
        html += f"""            <div class="rank-item">
                <div class="rank-number{top3_class}">#{rank}</div>
                <div class="keyword">{keyword_display}</div>
                <div class="pageviews">{pageviews:,} views</div>
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
    print("Generate Ranking Visualization")
    print("=" * 70)
    
    generate_json()
    generate_html()
    
    print()
    print("=" * 70)
    print("Visualization Completed")
    print("=" * 70)
