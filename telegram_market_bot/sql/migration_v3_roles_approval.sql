-- V3: rollar (mijoz / sotuvchi / admin), do'kon tasdiqlash (is_approved)
-- Supabase SQL Editor'da bir marta ishga tushiring.

-- Foydalanuvchi roli
alter table public.users drop constraint if exists users_role_check;
update public.users set role = 'customer' where role is null or role not in ('customer', 'seller', 'admin');
alter table public.users
  add constraint users_role_check
  check (role in ('customer', 'seller', 'admin'));
alter table public.users alter column role set default 'customer';
alter table public.users alter column role set not null;

-- Do'kon: tasdiq va rasmlar
alter table public.shops add column if not exists is_approved boolean default false;
alter table public.shops add column if not exists logo_url text;
alter table public.shops add column if not exists banner_url text;

-- Mavjud barcha do'konlarni tasdiqlangan deb belgilang (yangi sotuvchilar — false)
update public.shops set is_approved = true where true;

alter table public.shops alter column is_approved set default false;

-- Mahsulot rasmi
alter table public.products add column if not exists image_url text;
