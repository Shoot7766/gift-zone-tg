-- Supabase / PostgreSQL schema for Telegram marketplace bot
-- SQL Editor'da ishga tushiring (bir marta).

-- UUID uchun (Supabase odatda yoqilgan)
create extension if not exists "pgcrypto";

-- Foydalanuvchilar (Telegram profili)
create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  telegram_id bigint unique not null,
  username text,
  first_name text,
  last_name text,
  role text not null default 'customer',
  created_at timestamptz default now(),
  constraint users_role_check check (role in ('customer', 'seller', 'admin'))
);

create index if not exists idx_users_telegram_id on public.users (telegram_id);

-- Do'konlar
create table if not exists public.shops (
  id uuid primary key default gen_random_uuid(),
  owner_user_id uuid not null references public.users (id) on delete cascade,
  name text not null,
  description text,
  owner_telegram_username text,
  city text,
  logo_url text,
  banner_url text,
  is_approved boolean not null default false,
  subscription_type text default 'free',
  is_featured boolean default false,
  created_at timestamptz default now(),
  constraint shops_subscription_type_check
    check (subscription_type in ('free', 'pro', 'vip'))
);

create index if not exists idx_shops_owner on public.shops (owner_user_id);
create index if not exists idx_shops_subscription on public.shops (subscription_type);
create index if not exists idx_shops_featured on public.shops (is_featured desc);

-- Mahsulotlar
create table if not exists public.products (
  id uuid primary key default gen_random_uuid(),
  shop_id uuid not null references public.shops (id) on delete cascade,
  name text not null,
  description text,
  price numeric,
  category text,
  keywords text,
  image_url text,
  stock integer default 0,
  is_active boolean default true,
  created_at timestamptz default now()
);

create index if not exists idx_products_shop on public.products (shop_id);
create index if not exists idx_products_active on public.products (is_active);
create index if not exists idx_products_category on public.products (category);

-- Qidiruv jurnali
create table if not exists public.search_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users (id) on delete set null,
  user_query text,
  interpreted_query text,
  created_at timestamptz default now()
);

create index if not exists idx_search_logs_user on public.search_logs (user_id);
create index if not exists idx_search_logs_created on public.search_logs (created_at desc);

-- Saqlangan mahsulotlar (⭐)
create table if not exists public.user_favorites (
  user_id uuid not null references public.users (id) on delete cascade,
  product_id uuid not null references public.products (id) on delete cascade,
  created_at timestamptz default now(),
  primary key (user_id, product_id)
);

create index if not exists idx_favorites_user on public.user_favorites (user_id);

-- Row Level Security (ixtiyoriy): backend service_role kaliti RLSni aylanib o'tadi.
-- Agar faqat serverda ishlatsangiz, quyidagilarni yoqishingiz shart emas.

alter table public.users enable row level security;
alter table public.shops enable row level security;
alter table public.products enable row level security;
alter table public.search_logs enable row level security;
alter table public.user_favorites enable row level security;

-- Anon/authenticated uchun to'liq taqiq (bot Supabase "service_role" maxfiy kalitini ishlatadi)
drop policy if exists "deny anon users" on public.users;
drop policy if exists "deny anon shops" on public.shops;
drop policy if exists "deny anon products" on public.products;
drop policy if exists "deny anon search_logs" on public.search_logs;

create policy "deny anon users" on public.users for all using (false) with check (false);
create policy "deny anon shops" on public.shops for all using (false) with check (false);
create policy "deny anon products" on public.products for all using (false) with check (false);
create policy "deny anon search_logs" on public.search_logs for all using (false) with check (false);

drop policy if exists "deny anon user_favorites" on public.user_favorites;
create policy "deny anon user_favorites" on public.user_favorites
  for all using (false) with check (false);
