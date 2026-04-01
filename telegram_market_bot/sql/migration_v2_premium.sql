-- V2: premium do'konlar, saqlanganlar (migratsiya)
-- Avvalgi schema.sql ishlatilgan loyihada SQL Editor'da bir marta ishga tushiring.

alter table public.shops
  add column if not exists subscription_type text default 'free';

alter table public.shops
  add column if not exists is_featured boolean default false;

update public.shops set subscription_type = 'free' where subscription_type is null;
update public.shops set is_featured = false where is_featured is null;

alter table public.shops drop constraint if exists shops_subscription_type_check;
alter table public.shops
  add constraint shops_subscription_type_check
  check (subscription_type in ('free', 'pro', 'vip'));

create index if not exists idx_shops_subscription on public.shops (subscription_type);
create index if not exists idx_shops_featured on public.shops (is_featured desc);

-- Foydalanuvchi tanlagan mahsulotlar (⭐ Saqlash)
create table if not exists public.user_favorites (
  user_id uuid not null references public.users (id) on delete cascade,
  product_id uuid not null references public.products (id) on delete cascade,
  created_at timestamptz default now(),
  primary key (user_id, product_id)
);

create index if not exists idx_favorites_user on public.user_favorites (user_id);

alter table public.user_favorites enable row level security;
drop policy if exists "deny anon user_favorites" on public.user_favorites;
create policy "deny anon user_favorites" on public.user_favorites
  for all using (false) with check (false);
