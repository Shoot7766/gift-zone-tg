-- V4: mini ilova uchun bot orqali ro'yxatdan o'tish (telefon + rol)
-- Supabase SQL Editor'da bir marta ishga tushiring.

-- Telefon va ro'yxat holati
alter table public.users add column if not exists phone_number text;
alter table public.users add column if not exists is_registered boolean not null default false;
alter table public.users add column if not exists updated_at timestamptz default now();

-- Mavjud qatorlar: telefon va rol bo'lsa — ro'yxatdan o'tgan deb belgilash
update public.users
set is_registered = true
where coalesce(trim(phone_number), '') <> ''
  and role in ('customer', 'seller', 'admin');

-- updated_at avtomatik yangilanishi
create or replace function public.touch_users_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

drop trigger if exists users_touch_updated_at on public.users;
create trigger users_touch_updated_at
  before update on public.users
  for each row
  execute function public.touch_users_updated_at();
