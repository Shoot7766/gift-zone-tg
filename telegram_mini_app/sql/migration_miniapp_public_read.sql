-- Mini App (brauzer) uchun: anon kalit bilan faqat O'QISH.
-- Avvalgi schema "deny anon" bo'lsa, mahsulot va do'konlar uchun SELECT ruxsat beriladi.
-- Bot serveri service_role ishlatgani uchun o'zgarmaydi (RLS aylanib o'tadi).

-- Rasm ustunlari (yo'q bo'lsa)
alter table public.products add column if not exists image_url text;
alter table public.shops add column if not exists logo_url text;
alter table public.shops add column if not exists banner_url text;

-- Eski taqiqlovchi siyosatlarni olib tashlash (faqat products va shops)
drop policy if exists "deny anon products" on public.products;
drop policy if exists "deny anon shops" on public.shops;

-- Anon uchun faqat o'qish
drop policy if exists "miniapp_select_products" on public.products;
drop policy if exists "miniapp_select_shops" on public.shops;
drop policy if exists "miniapp_select_products_auth" on public.products;
drop policy if exists "miniapp_select_shops_auth" on public.shops;

create policy "miniapp_select_products"
  on public.products for select to anon
  using (coalesce(is_active, true) = true);

create policy "miniapp_select_shops"
  on public.shops for select to anon
  using (true);

-- Autentifikatsiyalangan Supabase foydalanuvchilari ham katalogni ko'ra olsin (ixtiyoriy)
create policy "miniapp_select_products_auth"
  on public.products for select to authenticated
  using (coalesce(is_active, true) = true);

create policy "miniapp_select_shops_auth"
  on public.shops for select to authenticated
  using (true);
