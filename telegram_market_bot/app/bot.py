"""python-telegram-bot Application ulanishi — faqat ro'yxatdan o'tish va mini ilova."""

import atexit
import logging
import os
from pathlib import Path

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

_LOCK_PATH = Path(__file__).resolve().parent.parent / ".telegram_bot_single.lock"


def _acquire_single_instance_lock() -> None:
    """Bitta polling — aks holda /start ga ikki marta javob (eski + yangi matn) keladi."""
    try:
        fd = os.open(_LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode("ascii", errors="replace"))
        os.close(fd)
    except FileExistsError:
        logger.error(
            "Bot allaqachon ishlamoqda yoki .telegram_bot_single.lock qoldi. "
            "Boshqa terminaldagi botni to'xtating yoki lock faylini o'chiring."
        )
        raise SystemExit(1)

    def _release() -> None:
        try:
            _LOCK_PATH.unlink(missing_ok=True)
        except OSError:
            pass

    atexit.register(_release)


async def _post_init(application: Application) -> None:
    """Webhook + polling aralashmasin."""
    await application.bot.delete_webhook(drop_pending_updates=False)
    info = await application.bot.get_me()
    logger.info("Bot: @%s (%s)", info.username or "?", info.first_name or "?")


def build_application() -> Application:
    app = (
        Application.builder()
        .token(config.TELEGRAM_BOT_TOKEN)
        .post_init(_post_init)
        .build()
    )

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

    _acquire_single_instance_lock()

    logger.info("Bot ishga tushmoqda...")
    application = build_application()
    application.run_polling()
