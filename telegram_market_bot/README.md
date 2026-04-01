# Gift Zone — Telegram kirish boti (Python)

Bu bot **Telegram Mini App** bozoriga kirish uchun soddalashtirilgan: foydalanuvchi telefon raqamini yuboradi, **mijoz** yoki **sotuvchi** sifatida tanlanadi, ma’lumotlar **Supabase** `users` jadvaliga yoziladi, so‘ng **mini ilovani ochish** tugmasi ko‘rsatiladi.

Barcha katalog, qidiruv va do‘kon boshqaruvi **mini ilovada**; bot faqat ro‘yxatdan o‘tish va yo‘l-yo‘riq uchun.

## Texnologiyalar

- **Python**, **python-telegram-bot** (polling)
- **Supabase** (PostgreSQL)
- **python-dotenv** (`.env`)

## Loyiha tuzilmasi

```
telegram_market_bot/
  app/
    bot.py       # Faqat kerakli handlerlar
    config.py    # .env (token, Supabase, MINI_APP_URL)
    db.py        # Supabase: foydalanuvchi, ro‘yxatdan o‘tish
    handlers.py  # /start, kontakt, rol, matn
    keyboards.py # Telefon, rol, Web App tugmasi
    ...          # admin_handlers, callbacks, seller_flow, ai — hozir bot ulanmagan
  sql/
    schema.sql              # Yangi o‘rnatish
    migration_v4_onboarding.sql  # Mavjud bazaga telefon + is_registered
    ...
  main.py
  requirements.txt
  .env.example
```

## Ro‘yxatdan o‘tish qanday ishlaydi

1. Foydalanuvchi **`/start`** yuboradi.
2. Agar bazada **telefon + rol** (mijoz/sotuvchi/admin) to‘liq bo‘lmasa, bot **«📱 Telefon raqamni yuborish»** tugmasi bilan kontaktni so‘raydi (faqat kontakt qabul qilinadi).
3. Kontakt kelgach, bot **«🛍 Mijoz»** yoki **«🏪 Sotuvchi»** tugmalarini beradi.
4. Tanlov **`customer`** yoki **`seller`** qiymati sifatida `users.role` ga yoziladi; telefon **`users.phone_number`** ga saqlanadi; **`is_registered`** `true` bo‘ladi.
5. Yakunda **«🚀 Gift Zone'ni ochish»** tugmasi chiqadi — bu Telegram **Web App** (`MINI_APP_URL`).

Agar foydalanuvchi allaqachon ro‘yxatdan o‘tgan bo‘lsa, qayta telefon so‘ralmaydi; qisqa **xush kelibsiz** va mini ilova tugmasi beriladi.

Telefon bor, rol yo‘q (kam uchraydigan holat) — faqat rol tanlanadi.

## Telefon raqami

Raqam faqat **kontakt yuborish** orqali olinadi (matn ko‘rinishida yozilgan raqam qabul qilinmaydi). Boshqa odamning kontakti bo‘lsa (`contact.user_id` boshqacha), bot xabar beradi.

## Rol qiymatlari

| Tugma        | Bazadagi `role` |
|-------------|------------------|
| 🛍 Mijoz    | `customer`       |
| 🏪 Sotuvchi | `seller`         |

`admin` roli faqat ma’lumotlar bazasida / boshqa vositalar orqali qo‘yilishi mumkin; bot faqat mijoz va sotuvchini tanlaydi.

## Mini ilova manzili qayerda

1. **`.env`** da **`MINI_APP_URL`** — to‘liq **HTTPS** manzil (masalan, Vercel’dagi Next.js mini app).
2. Telegram **@BotFather** da bot sozlamalarida **Mini App / Menu Button** uchun ham shu domen va URL mos kelishi kerak (Telegram talabi).

`MINI_APP_URL` bo‘lmasa yoki `https://` emas bo‘lsa, bot ishga tushmaydi (`validate_config`).

## Qaytgan foydalanuvchilar

`/start` da `users` qatorida **`phone_number`** to‘ldirilgan va **`role`** `customer` / `seller` / `admin` bo‘lsa, ro‘yxatdan o‘tgan hisoblanadi — bot darhol **mini ilovani ochish** tugmasini beradi va profil maydonlarini (username, ism) yangilab qo‘yadi.

## 1. Supabase

1. [supabase.com](https://supabase.com) da loyiha.
2. **Project Settings → API**: `SUPABASE_URL`, **service_role** secret → `SUPABASE_KEY` (faqat serverda).

## 2. SQL

- **Yangi loyiha:** `sql/schema.sql` ni bir marta ishga tushiring (ichida `users` uchun `phone_number`, `is_registered`, `updated_at` bor).
- **Mavjud baza (oldingi versiya):** `sql/migration_v4_onboarding.sql` ni ishga tushiring.
- Namuna ma’lumot: `sql/seed.sql` (ixtiyoriy).

## 3. `.env`

`.env.example` ni nusxalab `.env` qiling:

| O‘zgaruvchi | Ma’nosi |
|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | @BotFather |
| `SUPABASE_URL` | Supabase API URL |
| `SUPABASE_KEY` | **service_role** secret |
| `MINI_APP_URL` | Mini app **https://** manzili |

## 4. O‘rnatish va ishga tushirish

```bash
cd telegram_market_bot
python -m venv .venv
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Python **3.10+** tavsiya etiladi.

## Xavfsizlik

- `.env` ni git’ga qo‘shmang.
- `SUPABASE_KEY` faqat serverda saqlang.

## Muammolar

- **Bot ishga tushmaydi, MINI_APP_URL xato:** manzil `https://` bilan boshlanishi kerak.
- **Supabase xatoliklari:** `SUPABASE_URL` / `SUPABASE_KEY` (service_role) ni tekshiring.
- **Mini ilova ochilmaydagi:** BotFather’da domen tasdiqlanganmi va URL bir xilmi.

## Eslatma

`app/admin_handlers.py`, `callbacks.py`, `seller_flow.py`, `ai.py` fayllari repozitoriyda saqlanishi mumkin, lekin **joriy `bot.py` ularni ulanmaydi** — barcha bozor funksiyalari mini ilovaga ko‘chirilgan.
