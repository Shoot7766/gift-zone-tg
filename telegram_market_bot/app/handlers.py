"""Telegram command va matn handlerlari (o'zbekcha, premium UX)."""

import json
import logging
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes

from app import ai, config, db
from app.admin_handlers import is_admin_telegram
from app.keyboards import (
    customer_reply_keyboard,
    register_shop_tokens,
    role_pick_keyboard,
    search_results_keyboard,
    seller_reply_keyboard,
    shops_nav_keyboard,
    start_welcome_keyboard,
)
from app.seller_flow import (
    handle_customer_menu_text,
    handle_seller_menu_text,
    handle_seller_wizard_message,
)
from app.utils import (
    format_products_reply,
    format_search_intro,
    format_shop_line,
    format_welcome_header,
)

logger = logging.getLogger(__name__)

HELP_REPLY_HTML = (
    "<b>📌 Buyruqlar</b>\n"
    "<code>────────────────────</code>\n"
    "/start — boshlash (rol tanlash)\n"
    "/help — bu yordam\n"
    "/shops — do'konlar (premium tartibda)\n"
    "/products — yangi mahsulotlar\n"
    "<i>Sotuvchi:</i> <code>/mahsulot_off</code> — e'lonni yashirish\n\n"
    "<b>Qanday qidirish?</b>\n"
    "Oddiy gap yozing — AI so'rovingizni tushunadi, men esa bazadan "
    "mos mahsulotlarni chiqaraman.\n\n"
    "<b>Misol so'rovlar:</b>\n"
    "• sevganim uchun romantik sovg'a\n"
    "• arzon sovg'a quti\n"
    "• bola uchun ayiqcha\n"
    "• tadbir uchun bezak va sharlar\n\n"
    "<i>Savolingiz bo'lsa, bemalol yozing — yordam beraman.</i>"
)


async def send_role_main_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE, user_row: dict[str, Any]
) -> None:
    if not update.effective_user or not update.message:
        return
    u = update.effective_user
    if is_admin_telegram(u.id):
        await update.message.reply_html(
            "<b>👑 Administrator</b>\n\n"
            "/admin — statistika va kutilayotgan do‘konlar\n"
            "/approve_shop — do‘konni tasdiqlash\n"
            "/feature_shop — tavsiya (oldingi kabi)\n\n"
            "Mijozlar kabi qidiruvdan ham foydalanishingiz mumkin.",
            reply_markup=customer_reply_keyboard(),
        )
        return
    role = user_row.get("role") or "customer"
    if role == "seller":
        await update.message.reply_html(
            "<b>🏪 Siz do‘kon egasi sifatida tanlandingiz.</b>\n\n"
            "Pastdagi menyudan boshqaring — do‘kon, mahsulot va e’lonlar.",
            reply_markup=seller_reply_keyboard(),
        )
        return
    header = format_welcome_header(u.first_name)
    text = (
        f"{header}\n\n"
        "<b>🛍 Siz mijoz sifatida tanlandingiz.</b>\n"
        "• Sovg‘a va gul bo‘yicha <b>aqlli qidiruv</b>\n"
        "• <b>VIP / Pro</b> do‘konlar ustun\n"
        "• Sotuvchiga bir tugma bilan yozish\n\n"
        "<b>💡 Masalan yozing:</b>\n"
        "<i>«qizga sovg‘a kerak»</i>\n\n"
        "Pastdagi tugmalar yoki /help."
    )
    await update.message.reply_html(
        text,
        reply_markup=customer_reply_keyboard(),
    )


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    u = update.effective_user
    args = context.args or []

    row = db.get_user_by_telegram_id(u.id)
    if row:
        db.update_user_profile(
            telegram_id=u.id,
            username=u.username,
            first_name=u.first_name,
            last_name=u.last_name,
        )
        row = db.get_user_by_telegram_id(u.id)

    if row is None:
        await update.message.reply_html(
            "<b>Siz kim sifatida davom etmoqchisiz?</b>",
            reply_markup=role_pick_keyboard(),
        )
        return

    if args and args[0].lower() in ("seller", "sell", "sotuvchi"):
        if row.get("role") != "seller":
            await update.message.reply_html(
                "Bu havola faqat <b>do‘kon egalari</b> uchun. Siz mijoz sifatidasiz."
            )
            return
        await update.message.reply_html(
            "<b>🏪 Sotuvchi menyusi</b>",
            reply_markup=seller_reply_keyboard(),
        )
        return

    await send_role_main_menu(update, context, row)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_html(HELP_REPLY_HTML)


async def cmd_shops(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    shops = db.list_shops(limit=20)
    if not shops:
        await update.message.reply_html(
            "😕 <b>Hozircha do'konlar yo'q</b>\n\n"
            "Keyinroq qayta urinib ko'ring yoki qidiruv bilan yozing."
        )
        return
    lines = [
        "<b>🏪 Do'konlar</b>",
        "<i>VIP va tavsiya etilganlar yuqorida</i>\n",
        "<code>────────────────────</code>\n",
    ]
    for i, s in enumerate(shops, start=1):
        lines.append(format_shop_line(s, i))
        lines.append("")
    await update.message.reply_html(
        "\n".join(lines).strip(),
        reply_markup=shops_nav_keyboard(),
    )


async def cmd_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    u = update.effective_user
    products = db.list_latest_products(limit=8)
    if not products:
        await update.message.reply_html(
            "😕 <b>Mahsulotlar topilmadi</b>\n\n"
            "Keyinroq qayta tekshiring yoki qidiruv bilan yozing."
        )
        return
    user_row = db.update_user_profile(
        telegram_id=u.id,
        username=u.username,
        first_name=u.first_name,
        last_name=u.last_name,
    )
    uu = str(user_row["id"]) if user_row else ""
    pids = [str(p.get("id")) for p in products if p.get("id")]
    fav = db.favorited_map_for_user(uu, pids)
    smap = register_shop_tokens(products, context)
    body = format_products_reply(
        products,
        "So'nggi mahsulotlar",
        subtitle="Tanlangan do'konlar tartibi: VIP → Pro → Free",
    )
    await update.message.reply_html(
        body,
        reply_markup=search_results_keyboard(
            products,
            favorited_map=fav,
            shop_more_tokens=smap,
            has_more_in_session=False,
            include_more_prompt=False,
        ),
    )


def _interpreted_summary(interp: dict[str, Any]) -> str:
    try:
        return json.dumps(interp, ensure_ascii=False)
    except Exception:
        return str(interp)


async def cmd_mahsulot_off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    u = update.effective_user
    user_row = db.update_user_profile(
        telegram_id=u.id,
        username=u.username,
        first_name=u.first_name,
        last_name=u.last_name,
    )
    if not user_row or user_row.get("role") != "seller":
        await update.message.reply_html("Bu buyruq faqat <b>sotuvchilar</b> uchun.")
        return
    args = context.args or []
    if not args:
        await update.message.reply_html(
            "Format: <code>/mahsulot_off mahsulot_uuid</code>\n\n"
            "UUID ni <b>📦 Mahsulotlarim</b> ro‘yxatidan nusxalang."
        )
        return
    pid = args[0].strip()
    prod = db.get_product_by_id(pid)
    if not prod:
        await update.message.reply_html("Mahsulot topilmadi.")
        return
    sid = str(prod.get("shop_id") or "")
    if not db.shop_owned_by(sid, str(user_row["id"])):
        await update.message.reply_html("Bu mahsulot sizning do‘koningizga tegishli emas.")
        return
    if db.set_product_active_for_shop(pid, sid, False):
        await update.message.reply_html("✅ Mahsulot <b>faolsizlantirildi</b> (e’lon yashirildi).")
    else:
        await update.message.reply_html("😕 Yangilanmadi.")


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message or not update.message.text:
        return
    u = update.effective_user
    raw = update.message.text.strip()
    if raw.startswith("/"):
        return

    if await handle_seller_wizard_message(update, context):
        return

    user_row = db.update_user_profile(
        telegram_id=u.id,
        username=u.username,
        first_name=u.first_name,
        last_name=u.last_name,
    )
    if not user_row:
        user_row = db.get_user_by_telegram_id(u.id)
    if not user_row:
        await update.message.reply_html(
            "👋 Avval <b>/start</b> buyrug‘ini yuboring va rolni tanlang."
        )
        return

    role = user_row.get("role") or "customer"

    if role == "seller":
        if await handle_seller_menu_text(update, context, user_row):
            return
        await update.message.reply_html(
            "Menyudan tugmani tanlang yoki mahsulot qo‘shish bosqichidagi savollarga javob bering.\n"
            "Bozorda qidirish uchun: <b>🛒 Bozorga o‘tish</b>."
        )
        return

    if role == "customer":
        if await handle_customer_menu_text(update, context, user_row):
            return

    user_id = str(user_row["id"])

    await update.message.chat.send_action(action="typing")
    interp = ai.interpret_uzbek_request(raw)
    terms = list(interp.get("search_terms") or [])
    category = interp.get("category")

    db.log_search(
        user_id=user_id,
        user_query=raw,
        interpreted_query=_interpreted_summary(interp),
    )

    if not terms and not category:
        await update.message.reply_html(
            "🤔 <b>Tushunmadim</b>\n\n"
            "Iltimos, nimani izlayotganingizni <b>o'zbek tilida</b> qisqacha yozing.\n\n"
            "<i>Masalan:</i> <code>qizga sovg'a kerak</code>"
        )
        return

    limit = config.PRODUCT_SEARCH_LIMIT
    budget = interp.get("budget")
    fetch_limit = min(40, max(limit * 4, 20)) if budget else max(limit, 15)

    raw_products = db.search_products(
        search_terms=terms,
        category=category if category else None,
        limit=fetch_limit,
    )
    products = db.filter_by_budget(raw_products, budget) if budget else raw_products
    products = db.sort_products_by_shop_tier(products)
    products = products[:limit]

    if not products and raw_products and budget:
        await update.message.reply_html(
            f"😕 <b>Budjet bo'yicha topilmadi</b>\n\n"
            f"Siz ko'rsatgan <code>{budget}</code> so'm ichida mos mahsulot yo'q.\n"
            "Boshqa so'z bilan qidiring yoki budjetsiz yozing."
        )
        return

    if not products:
        await update.message.reply_html(
            "😕 <b>Hozircha mos mahsulot yo'q</b>\n\n"
            "Boshqa kalit so'zlar bilan urinib ko'ring — masalan:\n"
            "<i>gul</i>, <i>sovg'a quti</i>, <i>shar</i>, <i>tort</i>.\n\n"
            "Yoki /products buyrug'ini bosing."
        )
        return

    initial = max(1, min(config.SEARCH_INITIAL_SHOW, len(products)))
    shown = products[:initial]
    ids_all = [str(p["id"]) for p in products if p.get("id")]
    context.user_data["search_session"] = {
        "ids": ids_all,
        "offset": initial,
        "batch": config.SEARCH_MORE_BATCH,
        "query_text": raw[:500],
    }
    has_more = len(ids_all) > initial

    pids = [str(p.get("id")) for p in shown if p.get("id")]
    fav = db.favorited_map_for_user(user_id, pids)
    smap = register_shop_tokens(shown, context)

    intro = format_search_intro(raw)
    body = (
        intro
        + "\n\n"
        + format_products_reply(
            shown,
            f"Eng mos {len(shown)} ta natija",
            subtitle="⭐ VIP va tavsiya etilgan do'konlar avvalo",
        )
    )
    if has_more:
        body += (
            "\n\n<code>────────────────────</code>\n"
            "<b>❓ Yana variantlar ko'rsatilsinmi?</b>\n"
            "Pastdagi tugmalardan tanlang."
        )

    try:
        await update.message.reply_html(
            body,
            reply_markup=search_results_keyboard(
                shown,
                favorited_map=fav,
                shop_more_tokens=smap,
                has_more_in_session=has_more,
                include_more_prompt=has_more,
            ),
        )
    except Exception as e:
        logger.exception("reply_html failed: %s", e)
        await update.message.reply_html(
            "⚠️ <b>Formatda xatolik</b>\n\n"
            "Qayta urinib ko'ring yoki qisqaroq so'rov yuboring."
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Unhandled error: %s", context.error)
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_html(
                "😔 <b>Texnik nosozlik</b>\n\n"
                "Hozircha javob bera olmadim. Bir ozdan keyin qayta urinib ko'ring."
            )
        except Exception:
            pass
