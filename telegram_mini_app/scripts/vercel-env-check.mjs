/**
 * Vercel buildda NEXT_PUBLIC_* mavjudligini tekshiradi.
 * Mahalliy `npm run build` (.env.local) Next.js o‘zi o‘qiydi — bu yerda VERCEL bo‘lmasa hech narsa qilmaymiz.
 */
const isVercel = process.env.VERCEL === "1";
if (!isVercel) process.exit(0);

const url = (process.env.NEXT_PUBLIC_SUPABASE_URL || "").trim();
const key = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "").trim();

if (!url || !key) {
  console.warn(
    "\n⚠️ Vercel build: NEXT_PUBLIC_SUPABASE_URL yoki NEXT_PUBLIC_SUPABASE_ANON_KEY build vaqtida bo‘sh.\n" +
      "   (URL uzunligi: " +
      url.length +
      ", kalit uzunligi: " +
      key.length +
      ")\n" +
      "   Vercel → Project → Settings → Environment Variables: ikkalasini ham Production (+ kerak bo‘lsa Preview) ga qo‘shing, nomlarni Supabasedan nusxalang, keyin Redeploy.\n" +
      "   Build davom etadi, lekin saytda Supabase banner chiqadi — env to‘g‘rilanguncha.\n"
  );
  process.exit(0);
}

console.log("✓ Vercel: Supabase NEXT_PUBLIC_* build uchun mavjud.");
