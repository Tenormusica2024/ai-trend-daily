"""
設定ファイル - AI関連キーワードリスト
"""

# AI関連キーワードリスト（Wikipedia記事名）
# バズワード・急上昇ワード専用リスト（少数精鋭版）
AI_KEYWORDS = [
    # 2024-2025 新興AIサービス（厳選10個）
    "Perplexity.ai",
    "Mistral_AI",
    "Character.AI",
    "Cohere",
    "Stability_AI",
    "xAI",
    "Moonshot_AI",
    "Inflection_AI",
    "Poe_(chatbot)",
    "ElevenLabs",
    
    # 新興画像・動画AI（厳選5個）
    "Sora_(人工知能モデル)",  # Sora - 日本語版Wikipedia
    "Runway_(company)",
    "Kling_AI",
    "Luma_AI",
    "Synthesia",
    
    # 最新技術トレンド（厳選5個）
    "Agentic_AI",
    "Constitutional_AI",
    "Mixture_of_experts",
    "LoRA_(machine_learning)",
    "RLHF",
    
    # AIハードウェア（厳選3個）
    "Cerebras",
    "TPU",
    "Inferentia",
    
    # AI規制・倫理（厳選2個）
    "AI_alignment",
    "Superintelligence"
]

# 除外ワード（常連・基礎用語）- ランキングから完全除外
EXCLUDED_KEYWORDS = [
    "Artificial_intelligence",
    "ChatGPT",
    "GPT-4",
    "OpenAI",
    "Llama_(language_model)",
    "Large_language_model",
    "Machine_learning",
    "Deep_learning",
    "Neural_network",
    "Transformer_(machine_learning_model)",
    "Generative_artificial_intelligence",
    "Natural_language_processing",
    "Computer_vision",
    "Reinforcement_learning",
    "Anthropic",
    "Google_DeepMind",
    "Meta_AI",
    "Claude_(language_model)",
    "Gemini_(chatbot)",
    "Midjourney",
    "Stable_Diffusion",
    "DALL-E",
    # 追加除外（常連化したワード）
    "Grok_(chatbot)",  # Grok - 常連化
    "Retrieval-augmented_generation",  # RAG - 常連化
    "Groq"  # Groq - 常連化
]

# データベースパス
DB_PATH = "data/trends.db"

# 出力ファイルパス
OUTPUT_JSON = "output/ranking.json"
OUTPUT_HTML = "output/ranking.html"

# データ保持期間（日数）
DATA_RETENTION_DAYS = 60  # 60日平均計算用に延長

# Wikipedia API設定
USER_AGENT = "AI-Trend-Daily/1.0 (https://github.com/Tenormusica2024/ai-trend-daily)"
