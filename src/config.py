"""
設定ファイル - AI関連キーワードリスト
"""

# AI関連キーワードリスト（Wikipedia記事名）
# 常連ワード除外版 - 伸び率重視
AI_KEYWORDS = [
    "GPT-4",
    "Claude_(language_model)",
    "Gemini_(chatbot)",
    "Midjourney",
    "Stable_Diffusion",
    "DALL-E",
    "Runway_(company)",
    "Sora_(text-to-video_model)",
    "Generative_artificial_intelligence",
    "Deep_learning",
    "Anthropic",
    "Google_DeepMind",
    "GitHub_Copilot",
    "Prompt_engineering",
    "Perplexity.ai",
    "Mistral_AI",
    "Grok_(chatbot)",
    "Meta_AI",
    "Hugging_Face",
    "LangChain",
    "Vector_database",
    "Retrieval-augmented_generation",
    "Fine-tuning_(deep_learning)",
    "Transfer_learning",
    "Computer_vision",
    "Natural_language_processing",
    "Reinforcement_learning",
    "Agent_(artificial_intelligence)",
    "Multimodal_learning",
    "Diffusion_model"
]

# 除外ワード（常連・基礎用語）
EXCLUDED_KEYWORDS = [
    "Artificial_intelligence",
    "ChatGPT",
    "OpenAI",
    "Llama_(language_model)",
    "Large_language_model",
    "Machine_learning"
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
