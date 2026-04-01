"""Reply klaviaturalar — ro'yxatdan o'tish va mini ilova tugmasi."""

from telegram import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo


def phone_share_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def phone_and_role_keyboard() -> ReplyKeyboardMarkup:
    """/start: telefon + mijoz/sotuvchi bir ekranda (avval telefon, keyin rol)."""
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)],
            [KeyboardButton("🛍 Mijoz"), KeyboardButton("🏪 Sotuvchi")],
        ],
        resize_keyboard=True,
    )


def role_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🛍 Mijoz"), KeyboardButton("🏪 Sotuvchi")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def mini_app_open_keyboard(url: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton("🚀 Gift Zone'ni ochish", web_app=WebAppInfo(url=url))]],
        resize_keyboard=True,
    )
