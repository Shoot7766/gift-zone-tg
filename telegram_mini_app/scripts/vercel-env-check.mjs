/**
 * Vercel buildda NEXT_PUBLIC_* mavjudligini tekshiradi.
 * Mahalliy `npm run build` (.env.local) Next.js o‘zi o‘qiydi — bu yerda VERCEL bo‘lmasa hech narsa qilmaymiz.
 */
const isVercel = process.env.VERCEL === "1";
if (!isVercel) process.exit(0);

const url = (process.env.NEXT_PUBLIC_SUPABASE_URL || "").trim();
const key = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "").trim();

if (!url || !key) {
  console.error(
    "\n❌ Vercel build: NEXT_PUBLIC_SUPABASE_URL yoki NEXT_PUBLIC_SUPABASE_ANON_KEY topilmadi.\n" +
      "   Vercel → Project → Settings → Environment Variables:\n" +
      "   - Ikkala o‘zgaruvchi uchun ham Production (va kerak bo‘lsa Preview) belgilangan bo‘lsin.\n" +
      "   - Nomlar aynan shunday yozilsin (copy-paste).\n" +
      "   - Keyin Production deployni Redeploy qiling (mumkin bo‘lsa cache tozalab).\n" +
      "   Eslatma: faqat Preview URL (.vercel.app preview) ochsangiz — u Preview env ishlatadi, Production emas.\n"
  );
  process.exit(1);
}

console.log("✓ Vercel: Supabase NEXT_PUBLIC_* build uchun mavjud.");
