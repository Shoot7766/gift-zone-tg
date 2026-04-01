"""Formatting helpers for Telegram messages (Uzbek, premium HTML)."""

from typing import Any


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def uuid_to_callback_hex(product_id: str) -> str:
    return str(product_id).replace("-", "").lower()


def callback_hex_to_uuid(hex_id: str) -> str | None:
    h = (hex_id or "").strip().lower()
    if len(h) != 32:
        return None
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def shop_badges_line(shop: dict[str, Any]) -> str:
    """Do'kon uchun premium yorliqlar (VIP / tavsiya)."""
    parts: list[str] = []
    sub = str(shop.get("subscription_type") or "free").lower()
    if sub == "vip":
        parts.append("🔝 <b>Top do'kon</b>")
    elif sub == "pro":
        parts.append("💎 <b>Pro do'kon</b>")
    if shop.get("is_featured"):
        parts.append("⭐ <b>Tavsiya etiladi</b>")
    if not parts:
        return ""
    return " · ".join(parts)


def format_section_divider() -> str:
    return "\n<code>────────────────────</code>\n"


def format_product_block(
    product: dict[str, Any],
    index: int,
    *,
    compact_badges: bool = True,
) -> str:
    """Bitta mahsulot — tuzilgan, o'qish oson."""
    raw_shop = product.get("shops") or product.get("shop")
    shop = raw_shop if isinstance(raw_shop, dict) else {}
    shop_name = shop.get("name") or "Noma'lum do'kon"
    owner_username = shop.get("owner_telegram_username")

    badges = shop_badges_line(shop)
    badge_block = ""
    if badges and compact_badges:
        badge_block = f"\n<b>✨ Do'kon:</b> {badges}"

    name = _escape_html(str(product.get("name") or ""))
    desc = product.get("description") or "Tavsif qo'shilmoqda."
    desc = _escape_html(str(desc))
    price = product.get("price")
    if price is not None:
        try:
            price_str = f"{float(price):,.0f}".replace(",", " ")
        except (TypeError, ValueError):
            price_str = str(price)
    else:
        price_str = "kelishiladi"
    price_str = _escape_html(price_str)
    shop_name_esc = _escape_html(str(shop_name))

    contact_line = "Bog'lanish: hozircha username yo'q"
    if owner_username:
        u = str(owner_username).lstrip("@")
        contact_line = f'<a href="https://t.me/{_escape_html(u)}">@{_escape_html(u)}</a>'

    return (
        f"<b>🎁 Mahsulot #{index}</b>\n"
        f"{name}\n"
        f"{badge_block}\n\n"
        f"<b>📝 Tavsif</b>\n"
        f"{desc}\n\n"
        f"<b>💰 Narxi</b> · <code>{price_str}</code> so'm\n"
        f"<b>🏪 Do'kon</b> · {shop_name_esc}\n"
        f"<b>👤 Bog'lanish</b> · {contact_line}\n"
    )


def format_products_reply(
    products: list[dict[str, Any]],
    intro: str,
    *,
    subtitle: str | None = None,
) -> str:
    """Bir nechta mahsulot — bo'limlar bilan."""
    parts: list[str] = []
    parts.append(f"<b>{_escape_html(intro)}</b>")
    if subtitle:
        parts.append(f"<i>{_escape_html(subtitle)}</i>")
    parts.append("")
    for i, p in enumerate(products, start=1):
        if i > 1:
            parts.append(format_section_divider())
        parts.append(format_product_block(p, i))
    return "\n".join(parts).strip()


def format_shop_line(shop: dict[str, Any], index: int) -> str:
    name = _escape_html(str(shop.get("name") or ""))
    city = shop.get("city")
    city_part = f" · {_escape_html(str(city))}" if city else ""
    desc = shop.get("description") or ""
    desc = _escape_html(str(desc)[:180])
    owner = shop.get("owner_telegram_username")
    owner_part = ""
    if owner:
        u = str(owner).lstrip("@")
        owner_part = f'\n   👤 <a href="https://t.me/{_escape_html(u)}">@{_escape_html(u)}</a>'
    badges = shop_badges_line(shop)
    badge_line = f"\n   {badges}" if badges else ""
    sub = str(shop.get("subscription_type") or "free").lower()
    tier_emoji = {"vip": "🔝", "pro": "💎", "free": "📦"}.get(sub, "📦")
    return (
        f"{index}. {tier_emoji} <b>{name}</b>{city_part}{badge_line}\n"
        f"   <i>{desc}</i>{owner_part}"
    )


def format_welcome_header(first_name: str | None) -> str:
    if first_name and str(first_name).strip():
        who = _escape_html(str(first_name).strip())
    else:
        who = "mehmon"
    return (
        f"Assalomu alaykum, <b>{who}</b>! 👋\n\n"
        f"<b>Gift Zone</b> — sizning xarid yordamchingiz.\n"
        f"Sovg'a, gul, shar, tort va bezaklarni bir necha soniyada topamiz."
    )


def format_search_intro(query_hint: str) -> str:
    return (
        "<b>✅ Topildi</b>\n"
        f"<i>So'rovingiz:</i> {_escape_html(query_hint[:200])}"
    )
