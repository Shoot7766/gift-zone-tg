"""Load environment configuration for the bot."""

import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

# Load .env from project root (parent of app/)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)


def _normalize_bot_token(raw: str) -> str:
    t = raw.strip().strip('"').strip("'")
    if t.lower().startswith("bot "):
        t = t[4:].strip()
    return t


TELEGRAM_BOT_TOKEN = _normalize_bot_token(os.getenv("TELEGRAM_BOT_TOKEN", ""))
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

# Telegram Mini App HTTPS manzili (@BotFather → Bot Settings → Menu Button / Mini App)
MINI_APP_URL = os.getenv("MINI_APP_URL", "").strip()

# Admin Telegram ID lar (ixtiyoriy — boshqa modullar uchun saqlanadi)
_raw_admins = os.getenv("ADMIN_TELEGRAM_IDS", "").strip()
ADMIN_TELEGRAM_IDS: set[int] = set()
for part in _raw_admins.replace(" ", "").split(","):
    if part.isdigit():
        ADMIN_TELEGRAM_IDS.add(int(part))

# Legacy modullar (legacy/ papkasi) uchun ixtiyoriy — asosiy bot talab qilmaydi
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
PRODUCT_SEARCH_LIMIT = int(os.getenv("PRODUCT_SEARCH_LIMIT", "10"))
SEARCH_INITIAL_SHOW = int(os.getenv("SEARCH_INITIAL_SHOW", "3"))
SEARCH_MORE_BATCH = int(os.getenv("SEARCH_MORE_BATCH", "7"))
AUTO_APPROVE_SHOPS = os.getenv("AUTO_APPROVE_SHOPS", "false").strip().lower() in (
    "1",
    "true",
    "yes",
)


def _is_https_url(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme == "https" and bool(p.netloc)
    except Exception:
        return False


def validate_config() -> list[str]:
    """Return list of missing required variable names."""
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not SUPABASE_URL:
        missing.append("SUPABASE_URL")
    if not SUPABASE_KEY:
        missing.append("SUPABASE_KEY")
    if not MINI_APP_URL:
        missing.append("MINI_APP_URL")
    elif not _is_https_url(MINI_APP_URL):
        missing.append("MINI_APP_URL (https://... bo‘lishi kerak)")
    return missing
