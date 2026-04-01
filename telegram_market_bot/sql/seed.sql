-- Namuna ma'lumotlar (o'zbek sovg'a bozori temasi)
-- Avval schema.sql ishlatilgan bo'lishi kerak.
-- Takroriy ishlatish: pastdagi TRUNCATE qatorlarini oching (ehtiyotkorlik bilan).

-- truncate public.search_logs, public.products, public.shops, public.users cascade;

-- Do'kon egalari (Telegram ID lar — namuna)
insert into public.users (
  id, telegram_id, username, first_name, last_name, phone_number, role, is_registered
) values
  ('11111111-1111-4111-8111-111111111101', 900000001, 'gulmarket_owner', 'Malika', 'Karimova', '+998901111111', 'seller', true),
  ('22222222-2222-4222-8222-222222222202', 900000002, 'giftbox_uz', 'Jasur', 'Toshmatov', '+998902222222', 'seller', true),
  ('33333333-3333-4333-8333-333333333303', 900000003, 'partyfun_owner', 'Nodira', 'Yusupova', '+998903333333', 'seller', true)
on conflict (telegram_id) do nothing;

-- Do'konlar (VIP / Pro / Free namuna — premium tartibni sinash uchun)
insert into public.shops (
  id, owner_user_id, name, description, owner_telegram_username, city,
  subscription_type, is_featured, is_approved
) values
  (
    '44444444-4444-4444-8444-444444444401',
    '11111111-1111-4111-8111-111111111101',
    'Gul Market',
    'Yangi gul buketlari, romantik sovg''alar va yetkazib berish.',
    'gulmarket_owner',
    'Toshkent',
    'vip',
    true,
    true
  ),
  (
    '55555555-5555-4555-8555-555555555502',
    '22222222-2222-4222-8222-222222222202',
    'Sovg''a Box',
    'Tayyor sovg''a qutilari, shokolad va mayda sovg''alar.',
    'giftbox_uz',
    'Samarqand',
    'pro',
    false,
    true
  ),
  (
    '66666666-6666-4666-8666-666666666603',
    '33333333-3333-4333-8333-333333333303',
    'Party Fun',
    'Tadbir uchun sharlar, bezaklar va tortlar.',
    'partyfun_owner',
    'Toshkent',
    'free',
    false,
    true
  )
on conflict (id) do nothing;

-- Mahsulotlar (10 ta)
insert into public.products (id, shop_id, name, description, price, category, keywords, stock, is_active) values
  (
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaa0001',
    '44444444-4444-4444-8444-444444444401',
    'Qizil atirgul buketi',
    'Romantik sovg''a uchun chiroyli qizil atirgul buketi.',
    120000,
    'gullar',
    'gul atirgul buket romantik sevgi qizga sovg''a',
    15,
    true
  ),
  (
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaa0002',
    '44444444-4444-4444-8444-444444444401',
    'Oq lola guldasta',
    'To''y yoki tabrik uchun nafis oq lola guldastasi.',
    95000,
    'gullar',
    'lola gul guldasta to''y tabrik',
    20,
    true
  ),
  (
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaa0003',
    '55555555-5555-4555-8555-555555555502',
    'Yumshoq ayiqcha (katta)',
    '80 sm o''lchamdagi yumshoq ayiqcha — bola yoki qiz uchun.',
    180000,
    'oyinchoqlar',
    'ayiqcha yumshoq oyinchoq bola qiz sovg''a',
    8,
    true
  ),
  (
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaa0004',
    '55555555-5555-4555-8555-555555555502',
    'Sovg''a quti "Yurak"',
    'Shokolad va mayda shirinliklar bilan bezatilgan sovg''a quti.',
    75000,
    'sovg''alar',
    'sovg''a quti shokolad arzon romantik',
    30,
    true
  ),
  (
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaa0005',
    '66666666-6666-4666-8666-666666666603',
    'Helium sharlar to''plami (10 ta)',
    'Tug''ilgan kun yoki bayram uchun rang-barang sharlar.',
    55000,
    'sharlar',
    'shar helium bayram tug''ilgan kun tadbir',
    40,
    true
  ),
  (
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaa0006',
    '66666666-6666-4666-8666-666666666603',
    'Tug''ilgan kun torti 1 kg',
    'Vanil kremli, mevalar bilan bezatilgan tort.',
    220000,
    'tortlar',
    'tort tug''ilgan kun bayram shirinlik',
    12,
    true
  ),
  (
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaa0007',
    '55555555-5555-4555-8555-555555555502',
    'Konfetlar qutisi "Premium"',
    'Turli xil konfetlar — kichik sovg''a uchun qulay.',
    45000,
    'sovg''alar',
    'konfeta quti arzon sovg''a mayda',
    25,
    true
  ),
  (
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaa0008',
    '66666666-6666-4666-8666-666666666603',
    'LED romantik bezak to''plami',
    'Yorug''likli garland va yulduzchalar — uchrashuv uchun muhit.',
    65000,
    'bezaklar',
    'bezak led romantik muhit uchrashuv',
    18,
    true
  ),
  (
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaa0009',
    '44444444-4444-4444-8444-444444444401',
    'Atirgul + shokolad seti',
    '7 ta atirgul va belgiyalik shokolad — klassik kombinatsiya.',
    135000,
    'gullar',
    'atirgul shokolad set romantik sevgi',
    10,
    true
  ),
  (
    'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaa0010',
    '66666666-6666-4666-8666-666666666603',
    'Yangi yil / bayram archa bezagi',
    'Kichik archa va bezaklar to''plami.',
    89000,
    'bezaklar',
    'archa yangi yil bayram bezak uy',
    6,
    true
  )
on conflict (id) do nothing;
