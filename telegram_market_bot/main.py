"""
Gift Zone — Telegram kirish boti (ro'yxatdan o'tish + mini ilovaga yo'naltirish).
"""

import logging
import sys

from app.bot import run_bot

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        stream=sys.stdout,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    run_bot()


if __name__ == "__main__":
    main()
