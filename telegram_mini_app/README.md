# Gift Zone — Telegram Mini App (Next.js)

Premium ko‘rinishdagi **mahsulot va do‘konlar katalogi** — Telegram ichida ochiladi. Barcha UI matnlari **o‘zbekcha**. Backend sifatida **Supabase** ishlatiladi.

## Texnologiyalar

- Next.js 14 (App Router), TypeScript
- Tailwind CSS + shadcn/ui uslubidagi komponentlar
- `@supabase/supabase-js`
- Telegram Web App JS (`telegram-web-app.js`)

## O‘rnatish

```bash
cd telegram_mini_app
npm install
```

## Muhit o‘zgaruvchilari

`.env.local` yarating (`.env.example` dan nusxa):

```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOi...
```

- **anon / public** kalitdan foydalaning (`service_role` brauzerga qo‘ymang).

## Supabase sozlamalari (muhim)

1. **Rasm ustunlari** (ixtiyoriy): `sql/migration_miniapp_public_read.sql` fayli `image_url`, `logo_url`, `banner_url` qo‘shadi.
2. **RLS**: agar avval `deny anon` bo‘lsa, shu migratsiya mahsulot va do‘konlar uchun **anon SELECT** ochadi. Mini App ishlashi uchun migratsiyani Supabase SQL Editor’da ishga tushiring.

> Bot serveringiz `service_role` ishlatsa, u RLSni aylanib o‘tadi — migratsiya botni buzmaydi.

## Mahalliy ishga tushirish

```bash
npm run dev
```

Brauzer: [http://localhost:3000](http://localhost:3000)

HTTPS talabi tufayli Telegram ichida to‘liq test uchun tunnel kerak bo‘lishi mumkin (quyida).

## Telegram bot bilan ulash

1. [@BotFather](https://t.me/BotFather) → botingiz → **Bot Settings** → **Configure Menu Button** yoki **/setdomain** (Web App domeni).
2. **Keyboard** tugmasi qo‘shish (masalan `python-telegram-bot`):

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

Markup = InlineKeyboardMarkup([
    [InlineKeyboardButton(
        "🛍️ Katalogni ochish",
        web_app=WebAppInfo(url="https://SIZNING_DOMENINGIZ.vercel.app"),
    )]
])
```

3. Mini App URL **HTTPS** bo‘lishi kerak (Vercel, Cloudflare Tunnel, ngrok).

## Deploy (tavsiya: Vercel)

1. Reponi GitHubga yuklang.
2. [vercel.com](https://vercel.com) → Import → `NEXT_PUBLIC_*` o‘zgaruvchilarni qo‘shing.
3. Deploy tugagach, chiqan URL ni BotFather / WebApp tugmasiga qo‘ying.

## Loyiha tuzilishi

```
app/                 # Sahifalar (home, products, shops, favorites, search)
components/          # UI + marketplace komponentlari
components/ui/       # shadcn uslubi
lib/supabase/        # Klient va so‘rovlar
lib/telegram.ts      # WebApp yordamchilari
types/               # TypeScript turlari
sql/                 # Supabase migratsiya (anon o‘qish + rasm ustunlari)
```

## Favorites

Hozircha **localStorage** (`gift-zone-mini-favorites`). Keyinroq `user_favorites` jadvali bilan sinxron qilish mumkin.

## Vercel ishlamasa

Batafsil: **[VERCEL.md](./VERCEL.md)** — Root Directory, env, RLS.

## Savol-javob

**Nima uchun xato: “Ma'lumot yuklanmadi”?**  
`.env.local` yo‘q / noto‘g‘ri yoki Supabase’da anon uchun **SELECT** siyosati yo‘q.

**Bot va Mini App bir xil Supabase?**  
Ha, bir loyiha — bot `service_role`, Mini App `anon`.

---

Siz qo‘shishingiz kerak bo‘lgan env: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`.  
Botda: Web App tugmasiga deploy qilingan **HTTPS URL**.  
Mahalliy: `npm run dev`.  
Deploy: Vercel + xuddi shu env lar.
