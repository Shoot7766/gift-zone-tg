# Vercel — tez-tez uchraydigan muammolar (o‘zbekcha)

## 0. `404: NOT_FOUND` (sizda ko‘rinayotgan xato)

Bu xato **deyarli har doim** shuni anglatadi: Vercel butun repodan deploy qilyapti, lekin Next.js **`telegram_mini_app`** papkasida.

**Yechim (1 daqiqa):**

1. [vercel.com](https://vercel.com) → loyihangiz (**gift-zone-tg**)  
2. **Settings** → **General**  
3. **Root Directory** → **Edit**  
4. Yozing: **`telegram_mini_app`** (boshqa belgi qo‘ymang)  
5. **Save**  
6. **Deployments** → oxirgi deploy → **⋯** → **Redeploy**

Shundan keyin `gift-zone-tg.vercel.app` ochilishi kerak.

---

## 1. «Ishlamayapti» = sahifa ochilmaydi yoki build xato

### A) Root Directory (eng muhim)

Repoda **ikkita loyiha** bor: `telegram_market_bot` va `telegram_mini_app`.  
Vercel **faqat Next.js** papkasidan build qilishi kerak.

1. Vercel → **Project** → **Settings** → **General**
2. **Root Directory** → **Edit**
3. `telegram_mini_app` yozing (slashsiz)
4. **Save**
5. **Deployments** → so‘nggi deploy ustidagi **⋯** → **Redeploy**

Agar Root Directory bo‘sh yoki `gift zone tg` bo‘lsa, build topilmaydi yoki noto‘g‘ri chiqadi.

---

### B) «No Output Directory named public» xatosi

Vercel loyihani **Next.js** emas, oddiy statik sayt deb olgan.

1. **Settings** → **General** → **Framework Preset** → **Next.js** tanlang (Other / Static emas).
2. **Output Directory** maydoni **bo‘sh** qoldirilsin (Next.js uchun Vercel `.next` ni o‘zi biladi). Agar u yerda `public` yozilgan bo‘lsa — **o‘chirib** saqlang.
3. Loyihada `telegram_mini_app/vercel.json` bor — u `framework: nextjs` deb belgilangan; **Root Directory** = `telegram_mini_app` bo‘lishi kerak.
4. **Redeploy**.

---

### C) Environment Variables

1. **Settings** → **Environment Variables**
2. Quyidagilarni qo‘shing (Production, Preview, Development — keraklarini belgilang):

| Name | Qiymat |
|------|--------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase Project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | **anon public** kalit (service_role emas!) |

3. **Save** dan keyin **Redeploy** (env o‘zgarishlari eski deployda bo‘lmasligi mumkin).

---

### D) Supabase RLS

Mini App **anon** kalit bilan ishlaydi. Agar bazada faqat `deny anon` bo‘lsa, ma’lumot kelmaydi.

`telegram_mini_app/sql/migration_miniapp_public_read.sql` ni Supabase SQL Editor’da ishga tushiring.

---

### E) Build log

Vercel → **Deployments** → oxirgi deploy → **Building** log:

- `Could not find package.json` → Root Directory noto‘g‘ri
- `Module not found` → `npm ci` xato; `package-lock.json` repoda borligini tekshiring
- Boshqa xato matnini nusxalab qidirish yoki yuborish

---

## 2. Telegram ichida ochmayapti

- Mini App URL **HTTPS** bo‘lishi kerak (`https://....vercel.app`)
- BotFather da **Web App** uchun shu to‘liq manzil berilgan bo‘lsin

---

## 3. Qisqa checklist

- [ ] Root Directory = `telegram_mini_app`
- [ ] Framework Preset = **Next.js**, Output Directory **bo‘sh**
- [ ] `NEXT_PUBLIC_SUPABASE_*` Vercelda bor
- [ ] Deploydan keyin **Redeploy**
- [ ] `migration_miniapp_public_read.sql` ishlatilgan
