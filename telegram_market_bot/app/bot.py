"""python-telegram-bot Application ulanishi — faqat ro'yxatdan o'tish va mini ilova."""

import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from app import config
from app.handlers import (
    cmd_help,
    cmd_start,
    error_handler,
    handle_contact,
    handle_text_message,
)

logger = logging.getLogger(__name__)


def build_application() -> Application:
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    app.add_error_handler(error_handler)
    return app


def run_bot() -> None:
    missing = config.validate_config()
    if missing:
        logger.error("Yetishmayotgan yoki noto‘g‘ri o‘zgaruvchilar: %s", ", ".join(missing))
        raise SystemExit(1)

    logger.info("Bot ishga tushmoqda...")
    application = build_application()
    application.run_polling()
