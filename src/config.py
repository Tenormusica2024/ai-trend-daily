"""
設定ファイル - AI関連キーワードリスト
"""

# AI関連キーワードリスト（Wikipedia記事名）
# 30キーワードから20キーワードに削減（高速化）
AI_KEYWORDS = [
    "Artificial_intelligence",
    "ChatGPT",
    "GPT-4",
    "Claude_(language_model)",
    "Gemini_(chatbot)",
    "Midjourney",
    "Stable_Diffusion",
    "DALL-E",
    "Runway_(company)",
    "Sora_(text-to-video_model)",
    "Large_language_model",
    "Generative_artificial_intelligence",
    "Machine_learning",
    "Deep_learning",
    "OpenAI",
    "Anthropic",
    "Google_DeepMind",
    "Llama_(language_model)",
    "GitHub_Copilot",
    "Prompt_engineering"
]

# データベースパス
DB_PATH = "data/trends.db"

# 出力ファイルパス
OUTPUT_JSON = "output/ranking.json"
OUTPUT_HTML = "output/ranking.html"

# データ保持期間（日数）
DATA_RETENTION_DAYS = 7

# Wikipedia API設定
USER_AGENT = "AI-Trend-Daily/1.0 (https://github.com/Tenormusica2024/ai-trend-daily)"
