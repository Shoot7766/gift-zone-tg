"""
Telegram bot holatini tekshirish (webhook, bot nomi).
TOKEN ni .env dan o‘qiydi — hech narsani chatga yubormaydi.

Ishga tushirish (telegram_market_bot papkasidan):
  py -3 scripts/check_telegram.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# loyiha ildizi: telegram_market_bot/
ROOT = Path(__file__).resolve().parent.parent

# Telegram: raqamlar:harf-raqam (uzunlik har xil)
_TOKEN_RE = re.compile(r"^\d+:[A-Za-z0-9_-]+$")


def _normalize_token(raw: str) -> str:
    t = raw.strip().strip('"').strip("'")
    for prefix in ("bot ", "Bot ", "BOT "):
        if t.lower().startswith(prefix.lower()):
            t = t[len(prefix) :].strip()
    return t


def _print_401_help(token: str) -> None:
    print()
    print("401 Unauthorized = Telegram token not accepted.")
    print("Checklist:")
    print("  1) Open @BotFather -> your bot -> API Token (or /token)")
    print("  2) Copy the FULL line like: 123456789:AAH... (one colon, no spaces)")
    print("  3) In telegram_market_bot/.env single line: TELEGRAM_BOT_TOKEN=paste_here")
    print("  4) No quotes unless the whole value is quoted; save file as UTF-8")
    print("  5) If you revoked the old token, only the NEW token works")
    if not _TOKEN_RE.match(token):
        print()
        print("  [!] Token shape looks wrong (expected: digits:letters_and_digits)")
        print(f"      Length: {len(token)}, has colon: {':' in token}")


def main() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("pip install python-dotenv")
        sys.exit(1)

    load_dotenv(ROOT / ".env")
    token = _normalize_token(os.getenv("TELEGRAM_BOT_TOKEN", ""))
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN missing in .env")
        sys.exit(1)

    base = f"https://api.telegram.org/bot{token}"

    def call(method: str) -> dict:
        url = f"{base}/{method}"
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            print(f"HTTP {e.code}: {body[:500]}")
            if e.code == 401:
                _print_401_help(token)
            sys.exit(1)

    me = call("getMe")
    if not me.get("ok"):
        print("getMe:", me)
        sys.exit(1)
    r = me["result"]
    print("--- Bot ---")
    print(f"  @username: @{r.get('username', '?')}")
    print(f"  id: {r.get('id')}")
    print(f"  name: {r.get('first_name', '')}")

    wh = call("getWebhookInfo")
    if not wh.get("ok"):
        print("getWebhookInfo:", wh)
        sys.exit(1)
    w = wh["result"]
    print("--- Webhook ---")
    url = (w.get("url") or "").strip()
    if url:
        print(f"  URL: {url}")
        print("  [!] Webhook is ON - that server also receives updates. Do not mix with polling.")
        print("  To remove: open https://api.telegram.org/bot<TOKEN>/deleteWebhook in browser")
    else:
        print("  URL: (empty) - long polling only.")
    print(f"  pending_update_count: {w.get('pending_update_count', 0)}")
    print()
    print("--- If you get TWO replies to /start ---")
    print("  1) Another PC/VPS runs OLD bot with SAME token - stop it there.")
    print("  2) If webhook URL was set above - update or stop that server.")
    print("  3) Last resort: @BotFather -> Revoke token -> new token in ONE .env only.")


if __name__ == "__main__":
    main()
