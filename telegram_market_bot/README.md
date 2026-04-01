# Telegram marketplace yordamchi boti (Python)

O'zbek tilida ishlaydigan Telegram bot: foydalanuvchi so'rovini AI yordamida tahlil qiladi, Supabase'dagi mahsulotlarni qidiradi va tavsiyalar beradi.

## Texnologiyalar

- **Python**, **python-telegram-bot** (polling)
- **Supabase** (PostgreSQL)
- **OpenAI API** (faqat qidiruv parametrlarini ajratish uchun — mahsulotlar ixtiro qilinmaydi)
- **python-dotenv** (`.env`)

## Loyiha tuzilmasi

```
telegram_market_bot/
  app/
    bot.py            # Application
    config.py         # .env
    db.py             # Supabase (qidiruv, VIP tartib, admin, saqlanganlar)
    ai.py             # OpenAI + fallback
    handlers.py       # Buyruqlar va matnli qidiruv
    callbacks.py      # Inline tugmalar
    keyboards.py      # Klaviaturalar
    admin_handlers.py # /admin, /add_shop, ...
    utils.py          # HTML formatlash
  sql/
    schema.sql               # Jadvalar (yangi o'rnatish)
    migration_v2_premium.sql # Eski bazaga ustunlar + user_favorites
    seed.sql                 # Namuna ma'lumotlar
  main.py
  requirements.txt
  .env.example
```

## 1. Supabase loyihasini yaratish

1. [supabase.com](https://supabase.com) da yangi loyiha yarating.
2. **Project Settings → API** bo'limidan:
   - **Project URL** (`SUPABASE_URL`)
   - **service_role** **secret** kalit (`SUPABASE_KEY`) — faqat serverda, hech kimga ochiq qilmang.

## 2. SQL fayllarni ishga tushirish

1. Supabase konsolida **SQL Editor** ni oching.
2. `sql/schema.sql` ichidagi barcha matnni nusxalab, **Run** qiling (bir marta).
3. Agar loyiha **oldingi** versiya bo'lsa (do'konlarda `subscription_type` yo'q bo'lsa), `sql/migration_v2_premium.sql` ni ishga tushiring.
4. Keyin `sql/seed.sql` ni ishga tushiring (namuna do'konlar va mahsulotlar).

Agar seed'ni qayta tozalab yuklamoqchi bo'lsangiz, `seed.sql` dagi `truncate` qatorlaridagi izohlarni olib tashlang — ehtiyotkorlik bilan (barcha qatorlar o'chadi).

## 3. `.env` fayl

1. `telegram_market_bot` papkasida `.env` yarating (`.env.example` ni nusxalab nomini `.env` qiling).
2. Quyidagi o'zgaruvchilarni to'ldiring:

| O'zgaruvchi | Qayerdan |
|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Telegram **@BotFather** |
| `SUPABASE_URL` | Supabase loyiha URL |
| `SUPABASE_KEY` | Supabase **service_role** secret |
| `OPENAI_API_KEY` | OpenAI API kaliti |
| `ADMIN_TELEGRAM_IDS` | (ixtiyoriy) Sizning Telegram raqamingiz — `/admin` va boshqa admin buyruqlar uchun |

**Muhim:** `SUPABASE_KEY` sifatida **service_role** kalitini qo'ying. `schema.sql` da RLS yoqilgan; anon kalit bilan bot jadvalga yozolmaysiz.

## 4. Virtual muhit va kutubxonalar

```bash
cd telegram_market_bot
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Python **3.10+** tavsiya etiladi.

## 5. Botni ishga tushirish

```bash
python main.py
```

Konsolda `Bot ishga tushmoqda...` degan yozuvdan keyin Telegram'da botingizga yozing.

## Premium funksiyalar (qisqa)

- **Inline tugmalar:** sotuvchiga yozish, saqlash, yana variantlar, filtr/tavsiya.
- **Qidiruv:** avvalo **3 ta** eng mos natija, keyin «Yana variantlar?» (**Ha** / **Yo'q**).
- **Do'kon tartibi:** `vip` → `pro` → `free`; `is_featured=true` bo'lganlar o'z guruhida yuqorida.
- **⭐ Saqlash:** `user_favorites` jadvali (`migration_v2_premium.sql` yoki yangi `schema.sql`).

## Admin buyruqlar (faqat `ADMIN_TELEGRAM_IDS`)

| Buyruq | Vazifasi |
|--------|----------|
| `/admin` | Foydalanuvchilar, do'konlar, mahsulotlar, qidiruvlar soni |
| `/add_shop` | Yangi do'kon (buyruqni argumentssiz yuboring — format chiqadi) |
| `/add_product` | Yangi mahsulot |
| `/feature_shop` | ⭐ Tavsiya etiladi yoqish/o'chirish |
| `/set_sub` yoki `/set_subscription` | `free` / `pro` / `vip` |

## Namuna: foydalanuvchi oqimi (o'zbekcha)

1. `/start` — salom, maslahatlar va pastki tugmalar.
2. Matn: `qizga sovg'a kerak` — dastlab 3 ta mahsulot + tugmalar; ko'proq bo'lsa **Ha, yana variantlar**.
3. `/shops` — do'konlar (VIP / tavsiya belgilari bilan).
4. `/products` — so'nggi mahsulotlar + tugmalar.
5. `/help` — buyruqlar va misollar.

## Xavfsizlik qisqacha

- `.env` ni git'ga qo'shmang.
- `service_role` kalitini faqat serverda saqlang.
- OpenAI faqat foydalanuvchi matnidan **qidiruv parametrlarini** olish uchun ishlatiladi; mahsulotlar faqat bazadan olinadi.

## Muammolar

- **Supabase xatoliklari:** `SUPABASE_URL` / `SUPABASE_KEY` (service_role) ni tekshiring.
- **Hech narsa topilmaydi:** `seed.sql` ishlaganini va mahsulotlar `is_active = true` ekanini tekshiring.
- **Saqlash ishlamaydi:** `migration_v2_premium.sql` (yoki `user_favorites` jadvali) ishlatilganini tekshiring.
- **OpenAI ishlamasa:** bot avtomatik ravishda oddiy kalit so'zlarga o'tadi (`ai.py` ichidagi fallback).

## Keyingi qadamlar (ixtiyoriy)

- Sotuvchilar uchun mahsulot qo'shish (Telegram orqali yoki mini-admin).
- `get_shop_by_id` dan foydalanib, bitta do'kon kartochkasi ko'rsatish.
- Narxlarni filtrlash qoidalarini kengaytirish.
