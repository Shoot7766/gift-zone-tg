"""Admin / egasi buyruqlari (ADMIN_TELEGRAM_IDS)."""

import logging
import re

from telegram import Update
from telegram.ext import ContextTypes

from app import config, db

logger = logging.getLogger(__name__)


def is_admin_telegram(user_id: int | None) -> bool:
    if user_id is None:
        return False
    return user_id in config.ADMIN_TELEGRAM_IDS


async def cmd_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    if not is_admin_telegram(update.effective_user.id):
        await update.message.reply_html(
            "<b>⛔</b> Bu buyruq faqat administrator uchun."
        )
        return
    u, s, p, l = (
        db.count_users(),
        db.count_shops(),
        db.count_products(),
        db.count_search_logs(),
    )
    pending = db.list_pending_shops(12)
    pend_lines = ""
    if pending:
        pend_lines = "\n<b>⏳ Tasdiq kutilayotgan do‘konlar:</b>\n"
        for sh in pending:
            pend_lines += f"• <code>{sh.get('id')}</code> — {sh.get('name')}\n"
    else:
        pend_lines = "\n<i>Tasdiq kutilayotgan do‘kon yo‘q.</i>\n"

    text = (
        "<b>📊 Admin paneli</b>\n"
        "<code>────────────────────</code>\n"
        f"👥 Foydalanuvchilar: <b>{u}</b>\n"
        f"🏪 Do'konlar: <b>{s}</b>\n"
        f"🎁 Mahsulotlar: <b>{p}</b>\n"
        f"🔎 Qidiruvlar (jami): <b>{l}</b>\n"
        f"{pend_lines}\n"
        "<code>/approve_shop &lt;uuid&gt;</code> — do‘konni tasdiqlash"
    )
    await update.message.reply_html(text)


async def cmd_add_shop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    if not is_admin_telegram(update.effective_user.id):
        await update.message.reply_html("<b>⛔</b> Ruxsat yo'q.")
        return
    raw = " ".join(context.args or [])
    if not raw:
        await update.message.reply_html(
            "<b>➕ /add_shop</b>\n\n"
            "Format (ajratuvchi — <code>|</code>):\n"
            "<code>/add_shop egasi_telegram_id | do'kon_nomi | shahar | @username</code>\n\n"
            "<i>Misol:</i>\n"
            "<code>/add_shop 123456789 | Yangi Gul | Toshkent | yangi_gul</code>"
        )
        return
    parts = [x.strip() for x in raw.split("|")]
    if len(parts) < 4:
        await update.message.reply_html("😕 Yetarli maydon yo'q. <code>|</code> bilan 4 qism kiriting.")
        return
    tid_s, name, city, owner_u = parts[0], parts[1], parts[2], parts[3].lstrip("@")
    if not tid_s.isdigit():
        await update.message.reply_html("😕 Birinchi qism — egasining Telegram raqami (faqat raqam).")
        return
    owner_tid = int(tid_s)
    user_row = db.ensure_seller_user_for_admin(
        telegram_id=owner_tid,
        username=owner_u,
    )
    if not user_row:
        await update.message.reply_html("😕 Foydalanuvchini yaratib bo'lmadi.")
        return
    row = db.insert_shop(
        owner_user_id=str(user_row["id"]),
        name=name,
        description=None,
        city=city,
        owner_telegram_username=owner_u,
        subscription_type="free",
        is_featured=False,
        is_approved=True,
    )
    if row:
        await update.message.reply_html(
            f"✅ Do'kon qo'shildi.\n<b>ID:</b> <code>{row.get('id')}</code>"
        )
    else:
        await update.message.reply_html("😕 Saqlashda xato. Konsolni tekshiring.")


async def cmd_add_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    if not is_admin_telegram(update.effective_user.id):
        await update.message.reply_html("<b>⛔</b> Ruxsat yo'q.")
        return
    raw = " ".join(context.args or [])
    if not raw:
        await update.message.reply_html(
            "<b>➕ /add_product</b>\n\n"
            "Format:\n"
            "<code>/add_product do'kon_uuid | nom | narx | kategoriya | kalit_sozlar | tavsif</code>\n\n"
            "<i>Misol:</i>\n"
            "<code>/add_product uuid... | Sovg'a quti | 99000 | sovg'alar | quti arzon | Chiroyli quti</code>"
        )
        return
    if "|" not in raw:
        await update.message.reply_html("😕 <code>|</code> ajratuvchisidan foydalaning.")
        return
    shop_part, rest = raw.split("|", 1)
    shop_key = shop_part.strip()
    tail = [x.strip() for x in rest.split("|")]
    if len(tail) < 5:
        await update.message.reply_html("😕 5 ta qism kerak: nom, narx, kategoriya, kalit so'zlar, tavsif.")
        return
    name, price_s, cat, keys, desc = tail[0], tail[1], tail[2], tail[3], tail[4]
    try:
        price = float(re.sub(r"[^\d.]", "", price_s))
    except ValueError:
        await update.message.reply_html("😕 Narxni to'g'ri yozing (masalan: 120000).")
        return

    shop = None
    if re.match(
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
        shop_key,
    ):
        shop = db.get_shop_by_id(shop_key)
    if not shop:
        shop = db.find_shop_by_name_substring(shop_key)
    if not shop:
        await update.message.reply_html("😕 Do'kon topilmadi (UUID yoki nom bo'yicha).")
        return
    sid = str(shop["id"])
    row = db.insert_product(
        shop_id=sid,
        name=name,
        description=desc,
        price=price,
        category=cat,
        keywords=keys,
        stock=0,
    )
    if row:
        await update.message.reply_html(
            f"✅ Mahsulot qo'shildi.\n<b>ID:</b> <code>{row.get('id')}</code>"
        )
    else:
        await update.message.reply_html("😕 Saqlashda xato.")


async def cmd_feature_shop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    if not is_admin_telegram(update.effective_user.id):
        await update.message.reply_html("<b>⛔</b> Ruxsat yo'q.")
        return
    args = context.args or []
    if len(args) < 2:
        await update.message.reply_html(
            "<b>⭐ /feature_shop</b>\n\n"
            "<code>/feature_shop &lt;do'kon_uuid yoki nom&gt; on|off</code>\n\n"
            "<i>Misol:</i> <code>/feature_shop Gul Market on</code>"
        )
        return
    mode = args[-1].lower()
    key = " ".join(args[:-1]).strip()
    if mode not in ("on", "off", "true", "false", "1", "0"):
        await update.message.reply_html("😕 Oxirgi so'z: <code>on</code> yoki <code>off</code>.")
        return
    featured = mode in ("on", "true", "1")
    shop = None
    if re.match(
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
        key,
    ):
        shop = db.get_shop_by_id(key)
    if not shop:
        shop = db.find_shop_by_name_substring(key)
    if not shop:
        await update.message.reply_html("😕 Do'kon topilmadi.")
        return
    ok = db.set_shop_featured(str(shop["id"]), featured)
    if ok:
        await update.message.reply_html(
            f"✅ <b>{shop.get('name')}</b> — tavsiya: <b>{'yoqildi' if featured else 'ochirildi'}</b>."
        )
    else:
        await update.message.reply_html("😕 Yangilab bo'lmadi.")


async def cmd_approve_shop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    if not is_admin_telegram(update.effective_user.id):
        await update.message.reply_html("<b>⛔</b> Ruxsat yo‘q.")
        return
    args = context.args or []
    if not args:
        await update.message.reply_html(
            "<b>✅ /approve_shop</b>\n\n"
            "<code>/approve_shop &lt;do'kon_uuid&gt;</code>\n\n"
            "UUID ni /admin ro‘yxatidan oling."
        )
        return
    sid = args[0].strip()
    shop = db.get_shop_by_id(sid)
    if not shop:
        shop = db.find_shop_by_name_substring(sid)
    if not shop:
        await update.message.reply_html("😕 Do‘kon topilmadi.")
        return
    if db.set_shop_approved(str(shop["id"]), True):
        await update.message.reply_html(
            f"✅ <b>{shop.get('name')}</b> do‘koni <b>tasdiqlandi</b> — endi barcha mijozlarga ko‘rinadi."
        )
    else:
        await update.message.reply_html("😕 Yangilanmadi.")


async def cmd_set_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    if not is_admin_telegram(update.effective_user.id):
        await update.message.reply_html("<b>⛔</b> Ruxsat yo'q.")
        return
    args = context.args or []
    if len(args) < 2:
        await update.message.reply_html(
            "<b>💎 /set_sub</b> (yoki <code>/set_subscription</code>)\n\n"
            "<code>/set_sub &lt;uuid yoki nom&gt; free|pro|vip</code>\n\n"
            "VIP do'konlar qidiruvda birinchi chiqadi."
        )
        return
    tier = args[-1].lower()
    if tier not in ("free", "pro", "vip"):
        await update.message.reply_html("😕 Oxirgi so'z: <code>free</code>, <code>pro</code> yoki <code>vip</code>.")
        return
    key = " ".join(args[:-1]).strip()
    shop = None
    if re.match(
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
        key,
    ):
        shop = db.get_shop_by_id(key)
    if not shop:
        shop = db.find_shop_by_name_substring(key)
    if not shop:
        await update.message.reply_html("😕 Do'kon topilmadi.")
        return
    ok = db.set_shop_subscription(str(shop["id"]), tier)
    if ok:
        await update.message.reply_html(
            f"✅ <b>{shop.get('name')}</b> — obuna: <b>{tier.upper()}</b>."
        )
    else:
        await update.message.reply_html("😕 Yangilab bo'lmadi.")
