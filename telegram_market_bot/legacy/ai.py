"""OpenAI: Uzbek shopping intent → structured search parameters."""

import json
import logging
import re
from typing import Any

from openai import OpenAI

from app import config

logger = logging.getLogger(__name__)

INTERPRET_SYSTEM_PROMPT = """Sen O'zbekistondagi onlayn bozor yordamchisisan.
Foydalanuvchi o'zbek tilida yozgan so'rovni tahlil qil va FAQAT qidiruv parametrlarini JSON qaytarsan.
Hech qanday mahsulot nomini o'zingdan ixtiro qilma — faqat qidiruv uchun so'zlar va kategoriya.

Qoidalar:
- Barcha tushunchalarni foydalanuvchi tilida (o'zbekcha) aks ettir.
- "search_terms" — qisqa kalit so'zlar ro'yxati (2–8 ta), lotin yoki kirill bo'lishi mumkin.
- "category" — agar aniq bo'lsa mahsulot turkumi (masalan: gullar, sovg'alar, tortlar), yo'q bo'lsa null.
- "budget" — agar so'm/yirik raqam aytilsa raqam (butun son), aks holda null.

Javob FAQAT shu JSON sxemasida bo'lsin, boshqa matn yo'q:
{"search_terms": ["..."], "category": "..." | null, "budget": number | null}
"""


def _client() -> OpenAI:
    return OpenAI(api_key=config.OPENAI_API_KEY)


def fallback_from_text(user_text: str) -> dict[str, Any]:
    """Simple token-based fallback when OpenAI is unavailable."""
    cleaned = re.sub(r"[^\w\s\u0400-\u04FF']+", " ", user_text, flags=re.UNICODE)
    tokens = [t.strip() for t in cleaned.split() if len(t.strip()) > 1]
    # Drop very common filler words (Latin + some Cyrillic)
    stop = {
        "kerak", "uchun", "men", "menga", "bu", "va", "yoki", "qanday",
        "чун", "керак", "мен", "менга",
    }
    terms = [t for t in tokens[:12] if t.lower() not in stop]
    if not terms:
        terms = [user_text.strip()[:50]] if user_text.strip() else ["sovg'a"]
    return {
        "search_terms": terms[:8],
        "category": None,
        "budget": None,
    }


def interpret_uzbek_request(user_text: str) -> dict[str, Any]:
    """
    Return dict: search_terms (list[str]), category (str|None), budget (int|None).
    On API failure, uses fallback_from_text.
    """
    text = (user_text or "").strip()
    if not text:
        return {"search_terms": [], "category": None, "budget": None}

    try:
        client = _client()
        resp = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": INTERPRET_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Foydalanuvchi so'rovi:\n{text}",
                },
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=400,
        )
        raw = (resp.choices[0].message.content or "").strip()
        data = json.loads(raw)
        terms = data.get("search_terms") or []
        if isinstance(terms, str):
            terms = [terms]
        terms = [str(t).strip() for t in terms if str(t).strip()][:12]
        cat = data.get("category")
        category = str(cat).strip() if cat else None
        budget = data.get("budget")
        if budget is not None:
            try:
                budget = int(float(budget))
            except (TypeError, ValueError):
                budget = None
        return {
            "search_terms": terms,
            "category": category,
            "budget": budget,
        }
    except Exception as e:
        logger.warning("OpenAI interpret failed, using fallback: %s", e)
        return fallback_from_text(text)
