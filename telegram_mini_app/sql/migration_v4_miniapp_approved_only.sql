-- Mini App: faqat tasdiqlangan do'konlar va ularning faol mahsulotlari anon uchun ko'rinadi.
-- Avval migration_v3_roles_approval.sql ishlatilgan bo'lsin.

drop policy if exists "miniapp_select_products" on public.products;
drop policy if exists "miniapp_select_shops" on public.shops;
drop policy if exists "miniapp_select_products_auth" on public.products;
drop policy if exists "miniapp_select_shops_auth" on public.shops;

create policy "miniapp_select_shops"
  on public.shops for select to anon
  using (coalesce(is_approved, false) = true);

create policy "miniapp_select_products"
  on public.products for select to anon
  using (
    coalesce(is_active, true) = true
    and exists (
      select 1 from public.shops s
      where s.id = products.shop_id and coalesce(s.is_approved, false) = true
    )
  );

create policy "miniapp_select_shops_auth"
  on public.shops for select to authenticated
  using (coalesce(is_approved, false) = true);

create policy "miniapp_select_products_auth"
  on public.products for select to authenticated
  using (
    coalesce(is_active, true) = true
    and exists (
      select 1 from public.shops s
      where s.id = products.shop_id and coalesce(s.is_approved, false) = true
    )
  );
