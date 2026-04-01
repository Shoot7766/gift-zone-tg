# Gift Zone — Telegram kirish boti (Python)

Botning vazifasi: **ro‘yxatdan o‘tish** (telefon + mijoz/sotuvchi), ma’lumotni **Supabase** `users` jadvaliga yozish, **mini ilovani ochish** tugmasi.

Bozor, qidiruv, do‘kon boshqaruvi **mini ilovada**; bu bot faqat kirish.

## Tuzilma

```
telegram_market_bot/
  app/
    bot.py        # Polling, bitta nusxa qulfi, webhook tozalash
    config.py     # .env
    db.py         # Supabase (users + umumiy jadvallar)
    handlers.py   # /start, telefon, rol, /help
    keyboards.py  # Reply: telefon, mijoz/sotuvchi, Web App
    utils.py      # Legacy skriptlar uchun yordam (asosiy bot ishlatmaydi)
  legacy/         # Eski bozor modullari — bot ulanmaydi
  sql/
  main.py
  requirements.txt
  .env.example
```

## Oqim (o‘zbekcha matnlar)

1. **`/start`** — qisqa xush kelibsiz, **telefon tugmasi** + **🛍 Mijoz** / **🏪 Sotuvchi** (bir klaviaturada).
2. **Telefon** — **kontakt tugmasi** yoki **matn** (`+998901234567` yoki `998901234567`).
3. **«Rahmat, xizmatimizni tanlang.»** — faqat rol tugmalari.
4. Yakun — **«🚀 Gift Zone'ni ochish»** (`MINI_APP_URL`, HTTPS).

Ro‘yxatdan o‘tgan foydalanuvchi: qisqa xush kelibsiz + mini ilova tugmasi.

## `.env`

| O‘zgaruvchi | Ma’nosi |
|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | @BotFather |
| `SUPABASE_URL` | Supabase API URL |
| `SUPABASE_KEY` | **service_role** secret |
| `MINI_APP_URL` | Mini app **https://** manzili |

## SQL

- Yangi baza: `sql/schema.sql`
- Eski bazaga telefon / `is_registered`: `sql/migration_v4_onboarding.sql`

## Ishga tushirish

```bash
cd telegram_market_bot
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
python main.py
```

## Muhim

- **Bitta polling** — ikki `main.py` bir token bilan `/start` va telefon javoblarini **ikki marta** yoki **yo‘q** qiladi. `.telegram_bot_single.lock` bitta mashinada ikkinchi nusxani to‘xtatadi; **VPS + uy** ikkalasida ham bot bo‘lmasin.
- **Webhook** ishga tushganda avtomatik o‘chiriladi (polling bilan aralashmasin).

## Qayerdan bilaman (eski / ikkinchi javob kimdan?)

1. **Skript** (`.env` to‘ldirilgan bo‘lsin):

   ```bash
   cd telegram_market_bot
   py -3 scripts/check_telegram.py
   ```

   Chiqadi: bot `@username`, **webhook URL** (bo‘sh emas bo‘lsa — shu server ham xabarlarni oladi).

2. **Qo‘lda brauzer** (tokenni hech kimga bermang):

   `https://api.telegram.org/bot<TOKENINGIZ>/getWebhookInfo`  
   `url` maydoni bo‘sh bo‘lmasa — webhook ishlayapti.

3. **Windows**: Vazifalar boshqaruvchisida `python` / `py` jarayonlari — ikkita `main.py` bormi.

4. **VPS / hosting** — shu token bilan avval bot qo‘ygan bo‘lsangiz, u yerda ham to‘xtating yoki yangilang.

5. **Aniq ajratish**: @BotFather → **Revoke** token → yangi tokenni **faqat bitta** joydagi `.env` ga yozing (eski hamma joy to‘xtaydi).

## Xavfsizlik

`.env` va `SUPABASE_KEY` ni ochiq qilmang.
