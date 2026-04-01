"""Sotuvchi: do'kon va mahsulot (e'lon) yaratish oqimlari."""

import logging
import re
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes

from app import config, db

logger = logging.getLogger(__name__)

SHOP_W = "shop"
PROD_W = "product"


def _wizard(context: ContextTypes.DEFAULT_TYPE) -> dict[str, Any] | None:
    w = context.user_data.get("seller_wizard")
    return w if isinstance(w, dict) else None


def _clear_wizard(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop("seller_wizard", None)


def start_shop_wizard(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["seller_wizard"] = {
        "type": SHOP_W,
        "step": "name",
        "data": {},
    }


def start_product_wizard(context: ContextTypes.DEFAULT_TYPE, shop_id: str) -> None:
    context.user_data["seller_wizard"] = {
        "type": PROD_W,
        "step": "name",
        "shop_id": shop_id,
        "data": {},
    }


def _parse_price(text: str) -> float | None:
    s = re.sub(r"[^\d.]", "", text.strip())
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


async def handle_seller_wizard_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> bool:
    w = _wizard(context)
    if not w or not update.message or not update.message.text:
        return False
    text = update.message.text.strip()
    uid_row = db.get_user_by_telegram_id(update.effective_user.id) if update.effective_user else None
    if not uid_row or uid_row.get("role") != "seller":
        _clear_wizard(context)
        return False

    t = w.get("type")
    step = w.get("step")
    data: dict[str, Any] = w.get("data") or {}

    if t == SHOP_W:
        if step == "name":
            if len(text) < 2:
                await update.message.reply_html("😕 Nom juda qisqa. Yana yozing.")
                return True
            data["name"] = text[:200]
            w["data"] = data
            w["step"] = "desc"
            await update.message.reply_html(
                "<b>Do‘kon tavsifi</b>ni yozing (nima sotasiz, qisqacha)."
            )
            return True
        if step == "desc":
            data["description"] = text[:2000]
            w["data"] = data
            w["step"] = "city"
            await update.message.reply_html("<b>Shahar</b>ni yozing (masalan: Toshkent).")
            return True
        if step == "city":
            data["city"] = text[:120]
            w["data"] = data
            w["step"] = "username"
            await update.message.reply_html(
                "<b>Telegram username</b>ingizni yozing (masalan: <code>@dukan</code> yoki <code>dukan</code>).\n"
                "Agar hozir ko‘rsatmasangiz, <code>-</code> yuboring."
            )
            return True
        if step == "username":
            ou = None if text.strip() in ("-", "—", "yo‘q", "yoq") else text.strip().lstrip("@")[:64]
            approved = bool(config.AUTO_APPROVE_SHOPS)
            row = db.insert_shop(
                owner_user_id=str(uid_row["id"]),
                name=str(data.get("name") or ""),
                description=str(data.get("description") or ""),
                city=str(data.get("city") or ""),
                owner_telegram_username=ou,
                subscription_type="free",
                is_featured=False,
                is_approved=approved,
            )
            _clear_wizard(context)
            if not row:
                await update.message.reply_html("😕 Saqlashda xato. Keyinroq urinib ko‘ring.")
                return True
            if approved:
                await update.message.reply_html(
                    "✅ <b>Do‘koningiz yaratildi.</b> Endi mahsulot qo‘shishingiz mumkin.\n\n"
                    "➕ <b>Mahsulot qo‘shish</b> yoki <b>📢 E’lon berish</b> tugmasidan foydalaning."
                )
            else:
                await update.message.reply_html(
                    "✅ <b>So‘rovingiz qabul qilindi.</b>\n\n"
                    "Do‘koningiz <b>adminga yuborildi</b>. Tasdiqlangach barcha mijozlarga ko‘rinadi.\n\n"
                    "Tasdiqlanmaguncha mahsulot qo‘shishingiz mumkin — ular ham tasdiqlangan do‘kon bilan birga chiqadi."
                )
            return True

    if t == PROD_W:
        shop_id = str(w.get("shop_id") or "")
        if not shop_id or not db.shop_owned_by(shop_id, str(uid_row["id"])):
            _clear_wizard(context)
            await update.message.reply_html("⚠️ Do‘kon topilmadi. /start")
            return True

        if step == "name":
            if len(text) < 2:
                await update.message.reply_html("😕 Nom juda qisqa.")
                return True
            data["name"] = text[:200]
            w["data"] = data
            w["step"] = "desc"
            await update.message.reply_html("<b>Mahsulot tavsifi</b>ni yozing.")
            return True
        if step == "desc":
            data["description"] = text[:2000]
            w["data"] = data
            w["step"] = "price"
            await update.message.reply_html(
                "<b>Narx</b>ni yozing (faqat raqam, masalan: <code>120000</code>)."
            )
            return True
        if step == "price":
            price = _parse_price(text)
            if price is None:
                await update.message.reply_html("😕 Narxni raqam bilan yozing.")
                return True
            data["price"] = price
            w["data"] = data
            w["step"] = "category"
            await update.message.reply_html("<b>Kategoriya</b> (masalan: <code>Sovg‘a</code>, <code>Gullar</code>).")
            return True
        if step == "category":
            data["category"] = text[:120]
            w["data"] = data
            w["step"] = "image"
            await update.message.reply_html(
                "<b>Rasm havolasi</b> (URL) yoki o‘tkazib yuborish uchun <code>-</code>."
            )
            return True
        if step == "image":
            img = None if text.strip() in ("-", "—", "yo‘q", "yoq") else text.strip()[:2000]
            data["image_url"] = img
            w["data"] = data
            w["step"] = "stock"
            await update.message.reply_html(
                "<b>Ombordagi soni</b> (butun son) yoki <code>-</code> (0 deb olinadi)."
            )
            return True
        if step == "stock":
            st = 0
            if text.strip() not in ("-", "—", "yo‘q", "yoq"):
                try:
                    st = max(0, int(re.sub(r"\D", "", text) or 0))
                except ValueError:
                    st = 0
            name = str(data.get("name") or "")
            row = db.insert_product(
                shop_id=shop_id,
                name=name,
                description=str(data.get("description") or ""),
                price=float(data.get("price") or 0),
                category=str(data.get("category") or ""),
                keywords=name[:500],
                stock=st,
                image_url=data.get("image_url"),
            )
            _clear_wizard(context)
            if not row:
                await update.message.reply_html("😕 Saqlanmadi. Keyinroq urinib ko‘ring.")
                return True
            await update.message.reply_html(
                "✅ <b>Mahsulot muvaffaqiyatli qo‘shildi va e’lon sifatida joylandi.</b>\n\n"
                f"ID: <code>{row.get('id')}</code>"
            )
            return True

    return False


async def handle_seller_menu_text(
    update: Update, context: ContextTypes.DEFAULT_TYPE, user_row: dict[str, Any]
) -> bool:
    if not update.message or not update.message.text:
        return False
    text = update.message.text.strip()
    uid = str(user_row["id"])

    if text == "🏪 Do‘konim":
        shop = db.get_shop_by_owner_user_id(uid)
        if not shop:
            start_shop_wizard(context)
            await update.message.reply_html(
                "<b>Do‘kon hali yo‘q.</b>\n\n"
                "Keling, birga yaratamiz. <b>Do‘kon nomini</b> yozing:"
            )
            return True
        ap = shop.get("is_approved")
        st = "✅ Tasdiqlangan" if ap else "⏳ Admin tasdig‘i kutilmoqda"
        await update.message.reply_html(
            f"<b>🏪 {shop.get('name')}</b>\n"
            f"<b>Holat:</b> {st}\n"
            f"<b>Shahar:</b> {shop.get('city') or '—'}\n"
            f"<b>Tavsif:</b> {shop.get('description') or '—'}\n"
            f"<b>Kontakt:</b> @{shop.get('owner_telegram_username') or '—'}"
        )
        return True

    if text in ("➕ Mahsulot qo‘shish", "📢 E’lon berish"):
        shop = db.get_shop_by_owner_user_id(uid)
        if not shop:
            await update.message.reply_html(
                "Avval <b>🏪 Do‘konim</b> orqali do‘kon yarating."
            )
            return True
        start_product_wizard(context, str(shop["id"]))
        await update.message.reply_html(
            "<b>Yangi e’lon / mahsulot</b>\n\n"
            "<b>Mahsulot nomini</b> yozing:"
        )
        return True

    if text == "📦 Mahsulotlarim":
        shop = db.get_shop_by_owner_user_id(uid)
        if not shop:
            await update.message.reply_html("Do‘kon yo‘q.")
            return True
        prods = db.list_products_for_seller_shop(str(shop["id"]), 20)
        if not prods:
            await update.message.reply_html("Hozircha mahsulot yo‘q. <b>➕ Mahsulot qo‘shish</b> bosing.")
            return True
        lines = ["<b>📦 Sizning mahsulotlaringiz</b>\n"]
        for i, p in enumerate(prods, 1):
            act = "🟢" if p.get("is_active") else "⚪️"
            price = p.get("price")
            lines.append(
                f"{i}. {act} <b>{p.get('name')}</b> — {price} so‘m\n   <code>{p.get('id')}</code>"
            )
        lines.append(
            "\n<i>Faolsizlantirish uchun ID ni yozing:</i>\n<code>/mahsulot_off mahsulot_uuid</code>"
        )
        await update.message.reply_html("\n".join(lines))
        return True

    if text == "👤 Profilim":
        role = user_row.get("role")
        await update.message.reply_html(
            f"<b>Profil</b>\n"
            f"Rol: <b>{role}</b>\n"
            f"ID: <code>{user_row.get('id')}</code>"
        )
        return True

    if text == "🛒 Bozorga o‘tish":
        from app.keyboards import customer_reply_keyboard

        await update.message.reply_html(
            "<b>🛒 Mijoz rejimi</b>\n\n"
            "Mahsulotlarni qidiring — oddiy gap yozing.\n"
            "Sotuvchi menyusiga qaytish: tugmalardan <b>Profil</b> yoki /start",
            reply_markup=customer_reply_keyboard(),
        )
        return True

    return False


async def handle_customer_menu_text(
    update: Update, context: ContextTypes.DEFAULT_TYPE, user_row: dict[str, Any]
) -> bool:
    if not update.message or not update.message.text:
        return False
    text = update.message.text.strip()

    if text == "🎁 Sovg‘a topish":
        await update.message.reply_html(
            "<b>🔎 Qidiruv</b>\n\n"
            "O‘zbek tilida yozing — masalan:\n"
            "<i>qizga sovg‘a</i>, <i>gullar</i>, <i>tort</i>."
        )
        return True
    if text == "🛍 Mahsulotlar":
        from app.handlers import cmd_products

        await cmd_products(update, context)
        return True
    if text == "🏪 Do‘konlar":
        from app.handlers import cmd_shops

        await cmd_shops(update, context)
        return True
    if text == "⭐ Saqlanganlar":
        await update.message.reply_html(
            "<b>⭐ Saqlanganlar</b>\n\n"
            "Mini ilovada (Gift Zone) <b>Saqlanganlar</b> bo‘limini oching — "
            "u yerda yurakcha bilan saqlagan mahsulotlaringiz turadi."
        )
        return True
    if text == "📖 Yordam":
        from app.handlers import cmd_help

        await cmd_help(update, context)
        return True
    return False
