"""Load environment configuration for the bot."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (parent of app/)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# Search / AI tuning
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
PRODUCT_SEARCH_LIMIT = int(os.getenv("PRODUCT_SEARCH_LIMIT", "10"))

# Admin Telegram ID lar (vergul bilan): masalan 123456789,987654321
_raw_admins = os.getenv("ADMIN_TELEGRAM_IDS", "").strip()
ADMIN_TELEGRAM_IDS: set[int] = set()
for part in _raw_admins.replace(" ", "").split(","):
    if part.isdigit():
        ADMIN_TELEGRAM_IDS.add(int(part))

# Qidiruv natijasida birinchi xabarda ko'rsatiladigan mahsulotlar soni
SEARCH_INITIAL_SHOW = int(os.getenv("SEARCH_INITIAL_SHOW", "3"))
SEARCH_MORE_BATCH = int(os.getenv("SEARCH_MORE_BATCH", "7"))


def validate_config() -> list[str]:
    """Return list of missing required variable names."""
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not SUPABASE_URL:
        missing.append("SUPABASE_URL")
    if not SUPABASE_KEY:
        missing.append("SUPABASE_KEY")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    return missing
