"""Inline keyboardlar — premium UX."""

import secrets
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.utils import uuid_to_callback_hex


def register_shop_tokens(products: list[dict[str, Any]], context: Any) -> dict[str, str]:
    """hs:<token> uchun user_data ga shop_id + exclude mahsulot id saqlanadi."""
    out: dict[str, str] = {}
    for p in products:
        raw = p.get("shops") or p.get("shop")
        shop = raw if isinstance(raw, dict) else {}
        sid = str(shop.get("id") or "")
        pid = str(p.get("id") or "")
        if not sid or not pid:
            continue
        tok = secrets.token_hex(4)
        context.user_data[f"hs_{tok}"] = {"shop_id": sid, "exclude": pid}
        out[pid] = tok
    return out


def _shop_from_product(product: dict) -> dict:
    raw = product.get("shops") or product.get("shop")
    return raw if isinstance(raw, dict) else {}


# Callback qisqa prefikslar (Telegram 64 bayt cheklovi)
CB_FAV = "f"
CB_MORE_YES = "m:yes"
CB_MORE_NO = "m:no"
CB_NAV_SEARCH = "nav:search"
CB_NAV_TIP = "nav:tip"
CB_NAV_FILTER = "nav:filter"
CB_MORE_VIEW = "nav:more"
CB_SHOP_SESSION = "hs"
CB_WRITE_NONE = "wn"


def _fav_label(is_fav: bool) -> str:
    return "⭐ Saqlangan" if is_fav else "⭐ Saqlash"


def product_row_buttons(
    product: dict,
    index: int,
    *,
    favorited: bool,
    shop_more_token: str | None = None,
) -> list[list[InlineKeyboardButton]]:
    """Har bir mahsulot uchun qator tugmalar."""
    shop = _shop_from_product(product)
    pid = str(product.get("id") or "")
    ph = uuid_to_callback_hex(pid) if pid else ""
    row: list[InlineKeyboardButton] = []

    owner = (shop.get("owner_telegram_username") or "").strip().lstrip("@")
    if owner:
        row.append(
            InlineKeyboardButton(
                "📩 Sotuvchiga yozish",
                url=f"https://t.me/{owner}",
            )
        )
    else:
        row.append(
            InlineKeyboardButton(
                "📩 Sotuvchiga yozish",
                callback_data=f"{CB_WRITE_NONE}:{ph}" if ph else "wn:x",
            )
        )

    if ph:
        row.append(
            InlineKeyboardButton(
                _fav_label(favorited),
                callback_data=f"{CB_FAV}:{ph}",
            )
        )

    sid = str(shop.get("id") or "")
    shop_row: list[InlineKeyboardButton] = []
    if sid and shop_more_token:
        shop_row.append(
            InlineKeyboardButton(
                "📦 Boshqa mahsulotlar",
                callback_data=f"{CB_SHOP_SESSION}:{shop_more_token}",
            )
        )

    out = [row]
    if shop_row:
        out.append(shop_row)
    return out


def search_results_keyboard(
    products: list[dict],
    *,
    favorited_map: dict[str, bool],
    shop_more_tokens: dict[str, str] | None = None,
    has_more_in_session: bool = False,
    include_more_prompt: bool = True,
) -> InlineKeyboardMarkup:
    """Qidiruv / mahsulot ro'yxati uchun inline klaviatura."""
    rows: list[list[InlineKeyboardButton]] = []
    smap = shop_more_tokens or {}
    for i, p in enumerate(products, start=1):
        pid = str(p.get("id") or "")
        fav = favorited_map.get(pid, False)
        tok = smap.get(pid)
        rows.extend(
            product_row_buttons(p, i, favorited=fav, shop_more_token=tok)
        )

    rows.append(
        [
            InlineKeyboardButton("🔄 Yana qidirish", callback_data=CB_NAV_SEARCH),
            InlineKeyboardButton("💡 Tavsiya ber", callback_data=CB_NAV_TIP),
        ]
    )
    rows.append(
        [
            InlineKeyboardButton("🔎 Filtr qilish", callback_data=CB_NAV_FILTER),
            InlineKeyboardButton("📋 Yana ko'rish", callback_data=CB_MORE_VIEW),
        ]
    )
    if include_more_prompt and has_more_in_session:
        rows.append(
            [
                InlineKeyboardButton("✅ Ha, yana variantlar", callback_data=CB_MORE_YES),
                InlineKeyboardButton("❌ Yo'q, rahmat", callback_data=CB_MORE_NO),
            ]
        )
    return InlineKeyboardMarkup(rows)


def shops_nav_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔄 Yana qidirish", callback_data=CB_NAV_SEARCH),
                InlineKeyboardButton("💡 Tavsiya ber", callback_data=CB_NAV_TIP),
            ],
        ]
    )


def start_welcome_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📖 Yordam", callback_data="nav:help"),
                InlineKeyboardButton("🏪 Do'konlar", callback_data="nav:shops"),
            ],
            [
                InlineKeyboardButton("🛍️ Mahsulotlar", callback_data="nav:products"),
            ],
        ]
    )
