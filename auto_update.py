"""
自動更新メインスクリプト
データ収集 → ランキング生成を実行
"""
import sys
import os

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from collect_trends import collect_all_trends
from visualize_growth import generate_growth_json, generate_growth_html

def main():
    """メイン処理: データ収集 → 可視化"""
    try:
        # データ収集
        print("Starting AI Trend Data Collection...")
        top10 = collect_all_trends()
        
        if not top10:
            print("[ERROR] No data collected")
            return 1
        
        print("\n")
        
        # 可視化（伸び率ランキング）
        print("\nGenerating Growth Rate Visualization...")
        generate_growth_json()
        generate_growth_html()
        
        print("\n[SUCCESS] Auto-update completed")
        return 0
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
