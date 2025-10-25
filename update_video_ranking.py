#!/usr/bin/env python3
"""
動画生成AIランキング自動更新スクリプト
毎日定時実行でランキングデータを更新
"""

import json
import os
from datetime import datetime
from pathlib import Path

def update_video_ranking():
    """動画生成AIランキングデータを更新"""
    
    # 現在のディレクトリを取得
    script_dir = Path(__file__).resolve().parent
    output_file = script_dir / "video_ranking.json"
    
    # 更新日時
    current_time = datetime.now()
    updated_at = current_time.strftime("%Y-%m-%d %H:%M:%S JST")
    
    # ランキングデータ（実際の運用では外部APIやデータソースから取得）
    ranking_data = {
        "updated_at": updated_at,
        "ranking": [
            {
                "rank": 1,
                "name": "Sora 2",
                "company": "OpenAI",
                "url": "https://openai.com/sora",
                "description": "音声・効果音・セリフを映像と同期生成。Cameo機能で人物を任意のシーンに挿入可能"
            },
            {
                "rank": 2,
                "name": "Runway Gen-3",
                "company": "Runway",
                "url": "https://runwayml.com/",
                "description": "Motion Brushで動きをペイント指定。Act-One機能で実写から高品質アニメーション生成"
            },
            {
                "rank": 3,
                "name": "Pika",
                "company": "Pika Labs",
                "url": "https://www.pika.art/",
                "description": "Pikaframes機能で開始・終了フレームを指定し中間を自動生成。10秒1080p対応"
            },
            {
                "rank": 4,
                "name": "Stable Video Diffusion",
                "company": "Stability AI",
                "url": "https://stability.ai/",
                "description": "オープンソースで商用利用可。カスタマイズ性と低コスト運用が魅力"
            },
            {
                "rank": 5,
                "name": "Synthesia",
                "company": "Synthesia",
                "url": "https://www.synthesia.io/",
                "description": "企業研修・教育特化で240種類以上のAIアバター。SOC2/GDPR完全準拠で大企業導入実績"
            },
            {
                "rank": 6,
                "name": "HeyGen",
                "company": "HeyGen",
                "url": "https://www.heygen.com/",
                "description": "マーケティング動画特化で無制限生成可能。300種類の音声とカスタムアバター作成に強み"
            },
            {
                "rank": 7,
                "name": "Luma Dream Machine",
                "company": "Luma AI",
                "url": "https://lumalabs.ai/",
                "description": "Ray3エンジンで16bit HDR出力対応。10秒以内の超高速生成と4Kアップスケール"
            },
            {
                "rank": 8,
                "name": "NVIDIA VideoLDM",
                "company": "NVIDIA",
                "url": "https://www.nvidia.com/",
                "description": "研究レベルの最先端技術。長時間動画と高解像度出力の先駆者"
            },
            {
                "rank": 9,
                "name": "Descript Underlord",
                "company": "Descript",
                "url": "https://www.descript.com/",
                "description": "音声編集と統合。テキストベースで動画とオーディオを同時編集可能"
            },
            {
                "rank": 10,
                "name": "InVideo AI",
                "company": "InVideo",
                "url": "https://www.invideo.ai/",
                "description": "GPT-4連携でスクリプトから完全自動生成。Shopify/WooCommerce同期で商品動画を自動更新"
            }
        ]
    }
    
    # JSONファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(ranking_data, f, ensure_ascii=False, indent=2)
    
    print(f"OK Video AI Ranking updated: {updated_at}")
    print(f"Output file: {output_file}")
    
    return ranking_data

if __name__ == "__main__":
    update_video_ranking()
