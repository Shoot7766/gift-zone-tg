"""python-telegram-bot Application ulanishi."""

import logging

from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from app import config
from app.admin_handlers import (
    cmd_add_product,
    cmd_add_shop,
    cmd_admin,
    cmd_approve_shop,
    cmd_feature_shop,
    cmd_set_subscription,
)
from app.callbacks import handle_callback
from app.handlers import (
    cmd_help,
    cmd_products,
    cmd_shops,
    cmd_start,
    error_handler,
    handle_text_message,
)

logger = logging.getLogger(__name__)


def build_application() -> Application:
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("shops", cmd_shops))
    app.add_handler(CommandHandler("products", cmd_products))
    app.add_handler(CommandHandler("mahsulot_off", cmd_mahsulot_off))

    app.add_handler(CommandHandler("admin", cmd_admin))
    app.add_handler(CommandHandler("approve_shop", cmd_approve_shop))
    app.add_handler(CommandHandler("add_shop", cmd_add_shop))
    app.add_handler(CommandHandler("add_product", cmd_add_product))
    app.add_handler(CommandHandler("feature_shop", cmd_feature_shop))
    app.add_handler(CommandHandler("set_sub", cmd_set_subscription))
    app.add_handler(CommandHandler("set_subscription", cmd_set_subscription))

    app.add_handler(CallbackQueryHandler(handle_callback))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    app.add_error_handler(error_handler)
    return app


def run_bot() -> None:
    missing = config.validate_config()
    if missing:
        logger.error("Yetishmayotgan o'zgaruvchilar: %s", ", ".join(missing))
        raise SystemExit(1)

    if not config.ADMIN_TELEGRAM_IDS:
        logger.warning(
            "ADMIN_TELEGRAM_IDS bo'sh — /admin va boshqalar faqat .env da ID qo'shgandan keyin ishlaydi."
        )

    logger.info("Bot ishga tushmoqda...")
    application = build_application()
    application.run_polling()
