"""Ro'yxatdan o'tish: telefon, rol tanlash, mini ilovaga yo'naltirish (o'zbekcha)."""

import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from app import config, db
from app.keyboards import (
    mini_app_open_keyboard,
    phone_and_role_keyboard,
    role_reply_keyboard,
)

logger = logging.getLogger(__name__)

# Kontekst kalitlari
EXPECT = "onboarding_expect"
PENDING_PHONE = "pending_phone"

# Kutilgan qiymatlar
EXPECT_CONTACT = "contact"
EXPECT_CONTACT_EXISTING = "contact_existing"
EXPECT_ROLE = "role"
EXPECT_ROLE_EXISTING = "role_existing"

LABEL_MIJOZ = "🛍 Mijoz"
LABEL_SOTUVCHI = "🏪 Sotuvchi"

ONBOARDING_MSG_IDS = "onboarding_msg_ids"
MSG_ROLE_PROMPT = "Rahmat, xizmatimizni tanlang."


def _normalize_phone_input(text: str) -> str | None:
    """Bo'shliq va tireni olib tashlab, 9–15 raqam (+ ixtiyoriy boshida)."""
    compact = "".join(c for c in text.strip() if c.isdigit() or c == "+")
    if not compact:
        return None
    if compact.count("+") > 1 or ("+" in compact and not compact.startswith("+")):
        return None
    digits = "".join(c for c in compact if c.isdigit())
    if len(digits) < 9 or len(digits) > 15:
        return None
    return f"+{digits}" if compact.startswith("+") else digits


HELP_HTML = (
    "<b>Gift Zone — kirish boti</b>\n\n"
    "/start — ro'yxatdan o'tish yoki mini ilovani ochish\n\n"
    "Barcha bozor funksiyalari Telegram ichidagi <b>mini ilovada</b>."
)


def _clear_onboarding(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop(EXPECT, None)
    context.user_data.pop(PENDING_PHONE, None)
    context.user_data.pop(ONBOARDING_MSG_IDS, None)


async def _try_delete_message(
    context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int | None
) -> None:
    if message_id is None:
        return
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramError:
        pass


async def _delete_tracked_chat_messages(
    context: ContextTypes.DEFAULT_TYPE, chat_id: int
) -> None:
    ids = context.user_data.pop(ONBOARDING_MSG_IDS, None)
    if not ids:
        return
    for mid in ids:
        await _try_delete_message(context, chat_id, mid)


async def _send_onboarding_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *,
    text: str,
    reply_markup,
    track_user_command: bool = True,
) -> None:
    """Avvalgi onboarding xabarlarini o‘chiradi, yangisini yuboradi va id larni saqlaydi."""
    msg = update.message
    if not msg:
        return
    chat_id = msg.chat_id
    await _delete_tracked_chat_messages(context, chat_id)
    ids: list[int] = []
    if track_user_command:
        ids.append(msg.message_id)
    sent = await msg.reply_html(text, reply_markup=reply_markup)
    ids.append(sent.message_id)
    context.user_data[ONBOARDING_MSG_IDS] = ids


def _success_message() -> str:
    return (
        "✅ Ro'yxatdan o'tish muvaffaqiyatli yakunlandi.\n\n"
        "Endi platformadan foydalanish uchun quyidagi tugmani bosing:\n\n"
        "<i>Quyidagi tugma orqali Gift Zone mini ilovasini oching.</i>"
    )


def _welcome_back_message() -> str:
    return (
        "Qaytganingizdan xursandmiz!\n\n"
        "Platformaga kirish uchun quyidagi tugmani bosing:"
    )


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    u = update.effective_user
    msg = update.message

    row = db.get_user_by_telegram_id(u.id)
    if row:
        db.update_user_profile(
            telegram_id=u.id,
            username=u.username,
            first_name=u.first_name,
            last_name=u.last_name,
        )
        row = db.get_user_by_telegram_id(u.id)

    if row and db.user_registration_complete(row):
        _clear_onboarding(context)
        await msg.reply_html(
            _welcome_back_message(),
            reply_markup=mini_app_open_keyboard(config.MINI_APP_URL),
        )
        return

    has_phone = bool((row.get("phone_number") or "").strip()) if row else False
    role_val = row.get("role") if row else None
    has_valid_role = role_val in ("customer", "seller", "admin")

    if row and not has_phone:
        context.user_data[EXPECT] = EXPECT_CONTACT_EXISTING
        context.user_data.pop(PENDING_PHONE, None)
        await _send_onboarding_reply(
            update,
            context,
            text=(
                "Assalomu alaykum! Gift Zone'ga xush kelibsiz.\n\n"
                "Telefon raqamingizni yuboring, so‘ng rol tanlaysiz."
            ),
            reply_markup=phone_and_role_keyboard(),
        )
        return

    if row and has_phone and not has_valid_role:
        context.user_data[EXPECT] = EXPECT_ROLE_EXISTING
        await _send_onboarding_reply(
            update,
            context,
            text=MSG_ROLE_PROMPT,
            reply_markup=role_reply_keyboard(),
        )
        return

    # Yangi foydalanuvchi (bazada qator yo'q)
    context.user_data[EXPECT] = EXPECT_CONTACT
    context.user_data.pop(PENDING_PHONE, None)
    await _send_onboarding_reply(
        update,
        context,
        text=(
            "Assalomu alaykum! Gift Zone'ga xush kelibsiz.\n\n"
            "Telefon raqamingizni yuboring, so‘ng rol tanlaysiz."
        ),
        reply_markup=phone_and_role_keyboard(),
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_html(HELP_HTML)


async def _process_onboarding_phone(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    phone: str,
    *,
    remove_incoming_message: bool,
) -> bool:
    """
    Telefon qabul qilindi (kontakt yoki matn).
    True = onboarding bosqichi qayta ishlandi; False = /start kutilmoqda.
    """
    u = update.effective_user
    msg = update.message
    if not u or not msg:
        return False
    expect = context.user_data.get(EXPECT)
    chat_id = msg.chat_id

    if expect == EXPECT_CONTACT:
        await _delete_tracked_chat_messages(context, chat_id)
        context.user_data[PENDING_PHONE] = phone
        context.user_data[EXPECT] = EXPECT_ROLE
        sent = await msg.reply_html(MSG_ROLE_PROMPT, reply_markup=role_reply_keyboard())
        if remove_incoming_message:
            await _try_delete_message(context, chat_id, msg.message_id)
        context.user_data[ONBOARDING_MSG_IDS] = [sent.message_id]
        logger.info("onboarding: telefon qabul (yangi user), telegram_id=%s", u.id)
        return True

    if expect == EXPECT_CONTACT_EXISTING:
        updated = db.update_user_phone(u.id, phone)
        if not updated:
            await msg.reply_html(
                "Ma'lumotni saqlab bo'lmadi. Keyinroq /start orqali qayta urinib ko'ring."
            )
            return True
        await _delete_tracked_chat_messages(context, chat_id)
        if db.user_registration_complete(updated):
            await msg.reply_html(
                _success_message(),
                reply_markup=mini_app_open_keyboard(config.MINI_APP_URL),
            )
            if remove_incoming_message:
                await _try_delete_message(context, chat_id, msg.message_id)
            _clear_onboarding(context)
            logger.info("onboarding: telefon + ro'yxat tugallandi, telegram_id=%s", u.id)
            return True
        context.user_data[EXPECT] = EXPECT_ROLE_EXISTING
        sent = await msg.reply_html(MSG_ROLE_PROMPT, reply_markup=role_reply_keyboard())
        if remove_incoming_message:
            await _try_delete_message(context, chat_id, msg.message_id)
        context.user_data[ONBOARDING_MSG_IDS] = [sent.message_id]
        logger.info("onboarding: telefon saqlandi, rol kutilmoqda, telegram_id=%s", u.id)
        return True

    return False


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message or not update.message.contact:
        return
    u = update.effective_user
    msg = update.message
    contact = msg.contact
    expect = context.user_data.get(EXPECT)

    if contact.user_id is not None and contact.user_id != u.id:
        await msg.reply_html(
            "Bu boshqa foydalanuvchining kontakti. "
            "Iltimos, o'zingizning telefon raqamingizni yuboring."
        )
        return

    phone = (contact.phone_number or "").strip()
    if not phone:
        await msg.reply_html("Telefon raqamini o'qib bo'lmadi. Qayta urinib ko'ring.")
        return

    if await _process_onboarding_phone(
        update, context, phone, remove_incoming_message=True
    ):
        return

    logger.warning(
        "kontakt kutilmagan holatda: expect=%s telegram_id=%s",
        expect,
        u.id,
    )
    await msg.reply_html(
        "Avval /start buyrug'ini yuboring — keyin telefon yuboring."
    )


def _role_from_button(text: str) -> str | None:
    t = text.strip()
    if t == LABEL_MIJOZ:
        return "customer"
    if t == LABEL_SOTUVCHI:
        return "seller"
    return None


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message or not update.message.text:
        return
    u = update.effective_user
    msg = update.message
    raw = msg.text.strip()
    if raw.startswith("/"):
        return

    expect = context.user_data.get(EXPECT)
    role = _role_from_button(raw)

    if expect in (EXPECT_ROLE, EXPECT_ROLE_EXISTING) and role:
        chat_id = msg.chat_id
        if expect == EXPECT_ROLE:
            phone = (context.user_data.get(PENDING_PHONE) or "").strip()
            if not phone:
                await msg.reply_html(
                    "Avval telefon raqamingizni yuboring. /start"
                )
                return
            saved = db.insert_full_registration(
                telegram_id=u.id,
                username=u.username,
                first_name=u.first_name,
                last_name=u.last_name,
                phone_number=phone,
                role=role,
            )
            if not saved:
                await msg.reply_html(
                    "Ro'yxatdan o'tishda xatolik. Keyinroq qayta urinib ko'ring yoki /start."
                )
                return
            await _delete_tracked_chat_messages(context, chat_id)
            await _try_delete_message(context, chat_id, msg.message_id)
            _clear_onboarding(context)
            await context.bot.send_message(
                chat_id=chat_id,
                text=_success_message(),
                parse_mode=ParseMode.HTML,
                reply_markup=mini_app_open_keyboard(config.MINI_APP_URL),
            )
            return

        # EXPECT_ROLE_EXISTING
        saved = db.update_user_role_for_registration(u.id, role)
        if not saved:
            await msg.reply_html("Yangilab bo'lmadi. /start orqali qayta urinib ko'ring.")
            return
        await _delete_tracked_chat_messages(context, chat_id)
        await _try_delete_message(context, chat_id, msg.message_id)
        _clear_onboarding(context)
        await context.bot.send_message(
            chat_id=chat_id,
            text=_success_message(),
            parse_mode=ParseMode.HTML,
            reply_markup=mini_app_open_keyboard(config.MINI_APP_URL),
        )
        return

    if expect in (EXPECT_CONTACT, EXPECT_CONTACT_EXISTING):
        if role:
            await msg.reply_html(
                "Avval «📱 Telefon raqamni yuborish» tugmasi orqali raqamingizni yuboring, "
                "keyin «🛍 Mijoz» yoki «🏪 Sotuvchi»ni bosing."
            )
            return
        phone_text = _normalize_phone_input(raw)
        if phone_text:
            if await _process_onboarding_phone(
                update, context, phone_text, remove_incoming_message=True
            ):
                return
        await msg.reply_html(
            "Iltimos, «📱 Telefon raqamni yuborish» tugmasidan foydalaning "
            "yoki raqamingizni yozing: masalan <code>+998901234567</code> yoki <code>998901234567</code>.\n\n"
            "Agar javob kelmasa — avval <b>/start</b> yuboring."
        )
        return

    if expect in (EXPECT_ROLE, EXPECT_ROLE_EXISTING):
        await msg.reply_html(
            "Iltimos, «🛍 Mijoz» yoki «🏪 Sotuvchi» tugmalaridan birini tanlang."
        )
        return

    # Ro'yxatdan o'tgan — tasodifiy matn
    row = db.get_user_by_telegram_id(u.id)
    if row and db.user_registration_complete(row):
        await msg.reply_html(
            "Asosiy funksiyalar mini ilovada. Quyidagi tugma orqali oching:",
            reply_markup=mini_app_open_keyboard(config.MINI_APP_URL),
        )
        return

    await msg.reply_html("Davom etish uchun /start buyrug'ini yuboring.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Unhandled error: %s", context.error)
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_html(
                "Texnik nosozlik yuz berdi. Bir ozdan keyin qayta urinib ko'ring."
            )
        except Exception:
            pass
