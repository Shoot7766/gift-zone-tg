"""Inline callback handlerlar."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from app import config, db
from app.handlers import cmd_help, cmd_products, cmd_shops
from app.keyboards import register_shop_tokens, search_results_keyboard
from app.utils import (
    callback_hex_to_uuid,
    format_products_reply,
    format_search_intro,
)

logger = logging.getLogger(__name__)


async def _handle_role_pick(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data: str
) -> None:
    q = update.callback_query
    if not q or not q.from_user or not q.message:
        return
    role = data.split(":", 1)[-1].strip()
    if role not in ("customer", "seller"):
        await q.answer()
        return
    existing = db.get_user_by_telegram_id(q.from_user.id)
    if existing:
        await q.answer("Siz allaqachon ro‘yxatdan o‘tgansiz.", show_alert=True)
        return
    row = db.create_user_with_role(
        telegram_id=q.from_user.id,
        username=q.from_user.username,
        first_name=q.from_user.first_name,
        last_name=q.from_user.last_name,
        role=role,
    )
    await q.answer()
    try:
        await q.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    if not row:
        await q.message.reply_html("😕 Ro‘yxatdan o‘tishda xato. /start ni qayta yuboring.")
        return
    from app.keyboards import customer_reply_keyboard, seller_reply_keyboard

    if role == "customer":
        await q.message.reply_html(
            "<b>🛍 Siz mijoz sifatida tanlandingiz.</b>\n\n"
            "Mahsulotlarni qidiring yoki pastdagi tugmalardan foydalaning.",
            reply_markup=customer_reply_keyboard(),
        )
    else:
        await q.message.reply_html(
            "<b>🏪 Siz do‘kon egasi sifatida tanlandingiz.</b>\n\n"
            "<b>🏪 Do‘konim</b> tugmasi bilan do‘kon yarating, keyin mahsulot qo‘shing.",
            reply_markup=seller_reply_keyboard(),
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    if not q or not q.data or not q.message:
        return
    data = q.data

    if data.startswith("role:"):
        await _handle_role_pick(update, context, data)
        return

    if data == "m:yes":
        await _more_search_yes(update, context)
        return

    if data == "m:no":
        await q.answer("Rahmat!")
        await q.message.reply_html(
            "<b>👍 Yaxshi!</b>\n\n"
            "Keyinroq yana qidirish uchun oddiy gap yozing — masalan:\n"
            "<i>qizga sovg'a kerak</i> yoki <i>gullar</i>."
        )
        return

    if data == "nav:search":
        await q.answer()
        await q.message.reply_html(
            "<b>🔎 Yana qidirish</b>\n\n"
            "Nima qidiryapsiz? Qisqa yozing — masalan:\n"
            "• <i>arzon sovg'a</i>\n• <i>gullar</i>\n• <i>tug'ilgan kun torti</i>"
        )
        return

    if data == "nav:tip":
        await q.answer()
        await q.message.reply_html(
            "<b>💡 Tavsiyalar</b>\n\n"
            "• <i>sevganim uchun romantik sovg'a</i>\n"
            "• <i>bola uchun yumshoq o'yinchoq</i>\n"
            "• <i>tadbir uchun shar va bezak</i>\n\n"
            "Vaziyatni o'zbek tilida yozing — men mos variantlarni topaman."
        )
        return

    if data == "nav:filter":
        await q.answer()
        await q.message.reply_html(
            "<b>🔎 Filtr</b>\n\n"
            "Tez orada narx va shahar bo'yicha filtrlash paydo bo'ladi.\n"
            "Hozir <b>arzon</b>, <b>gul</b>, <b>tort</b> kabi so'zlar bilan "
            "qayta yozing — natija aniqroq bo'ladi."
        )
        return

    if data == "nav:more":
        await _more_search_yes(update, context)
        return

    if data == "nav:help":
        await q.answer()
        nu = Update(update_id=update.update_id, message=q.message)
        await cmd_help(nu, context)
        return

    if data == "nav:shops":
        await q.answer()
        nu = Update(update_id=update.update_id, message=q.message)
        await cmd_shops(nu, context)
        return

    if data == "nav:products":
        await q.answer()
        nu = Update(update_id=update.update_id, message=q.message)
        await cmd_products(nu, context)
        return

    if data.startswith("wn:"):
        await q.answer(
            "Bu sotuvchining Telegram username'i hozircha yo'q. "
            "Do'kon bo'yicha /shops dan qarang.",
            show_alert=True,
        )
        return

    if data.startswith("f:"):
        await _toggle_favorite(q, context, data)
        return

    if data.startswith("hs:"):
        await _shop_more(q, context, data)
        return

    await q.answer()


async def _toggle_favorite(q, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
    hex_part = data.split(":", 1)[-1].strip()
    pid = callback_hex_to_uuid(hex_part)
    if not pid or not q.from_user:
        await q.answer("Xatolik.", show_alert=True)
        return
    user_row = db.update_user_profile(
        telegram_id=q.from_user.id,
        username=q.from_user.username,
        first_name=q.from_user.first_name,
        last_name=q.from_user.last_name,
    )
    if not user_row:
        await q.answer("Avval /start — rolni tanlang.", show_alert=True)
        return
    uid = str(user_row["id"])
    ok, now_fav = db.toggle_favorite(uid, pid)
    if not ok:
        await q.answer(
            "Saqlash ishlamadi. Bazada user_favorites jadvali bormi? (migration_v2)",
            show_alert=True,
        )
        return
    await q.answer("⭐ Saqlandi!" if now_fav else "Olib tashlandi.")


async def _shop_more(q, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
    tok = data.split(":", 1)[-1].strip()
    ctx = context.user_data.get(f"hs_{tok}")
    if not isinstance(ctx, dict):
        await q.answer("Ma'lumot eskirgan. Qayta qidiring.", show_alert=True)
        return
    shop_id = str(ctx.get("shop_id") or "")
    exclude = str(ctx.get("exclude") or "")
    if not shop_id:
        await q.answer("Do'kon topilmadi.", show_alert=True)
        return
    more = db.list_more_products_from_shop(shop_id, exclude, limit=5)
    if not more:
        await q.answer("Boshqa mahsulot yo'q.", show_alert=True)
        return
    if not q.from_user or not q.message:
        return
    user_row = db.update_user_profile(
        telegram_id=q.from_user.id,
        username=q.from_user.username,
        first_name=q.from_user.first_name,
        last_name=q.from_user.last_name,
    )
    uu = str(user_row["id"]) if user_row else ""
    pids = [str(x.get("id")) for x in more if x.get("id")]
    fav = db.favorited_map_for_user(uu, pids)
    smap = register_shop_tokens(more, context)
    body = format_products_reply(
        more,
        "Shu do'kondan boshqa mahsulotlar:",
        subtitle="Tanlanganidan tashqari",
    )
    await q.message.reply_html(
        body,
        reply_markup=search_results_keyboard(
            more,
            favorited_map=fav,
            shop_more_tokens=smap,
            has_more_in_session=False,
            include_more_prompt=False,
        ),
    )
    await q.answer()


async def _more_search_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    if not q or not q.message:
        return
    sess = context.user_data.get("search_session")
    if not isinstance(sess, dict):
        await q.answer("Avval qidiruv yozing.", show_alert=True)
        return
    ids: list[str] = [str(x) for x in (sess.get("ids") or [])]
    offset = int(sess.get("offset") or 0)
    batch = int(sess.get("batch") or config.SEARCH_MORE_BATCH)
    if offset >= len(ids):
        await q.answer("Boshqa variantlar yo'q.", show_alert=True)
        return
    chunk = ids[offset : offset + batch]
    sess["offset"] = offset + len(chunk)
    context.user_data["search_session"] = sess

    products = db.get_products_by_ids(chunk)
    if not products:
        await q.answer("Yuklanmadi.", show_alert=True)
        return

    if not q.from_user:
        return
    user_row = db.update_user_profile(
        telegram_id=q.from_user.id,
        username=q.from_user.username,
        first_name=q.from_user.first_name,
        last_name=q.from_user.last_name,
    )
    uu = str(user_row["id"]) if user_row else ""
    pids = [str(p.get("id")) for p in products if p.get("id")]
    fav = db.favorited_map_for_user(uu, pids)
    smap = register_shop_tokens(products, context)
    has_more = sess["offset"] < len(ids)

    intro = format_search_intro(str(sess.get("query_text") or "qidiruv"))
    body = (
        intro
        + "\n\n"
        + format_products_reply(
            products,
            f"Yana {len(products)} ta variant",
            subtitle="VIP va tavsiya etilgan do'konlar avvalo",
        )
    )
    await q.message.reply_html(
        body,
        reply_markup=search_results_keyboard(
            products,
            favorited_map=fav,
            shop_more_tokens=smap,
            has_more_in_session=has_more,
            include_more_prompt=True,
        ),
    )
    await q.answer()
