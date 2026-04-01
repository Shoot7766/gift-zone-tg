import type { Product, Shop } from "@/types";

const DEMO_SHOP_GIFT: Shop = {
  id: "demo-shop-gift",
  name: "Sovg‘a Studio",
  description: "Premium sovg‘alar va qadoqlash",
  owner_telegram_username: null,
  city: "Toshkent",
  logo_url: null,
  banner_url: null,
  subscription_type: "vip",
  is_featured: true,
};

const DEMO_SHOP_FLOWERS: Shop = {
  id: "demo-shop-flowers",
  name: "Gul Galereyasi",
  description: "Yashil gullar va buketlar",
  owner_telegram_username: null,
  city: "Samarqand",
  logo_url: null,
  banner_url: null,
  subscription_type: "pro",
  is_featured: true,
};

const DEMO_SHOP_SWEET: Shop = {
  id: "demo-shop-sweet",
  name: "Shirinlik Uyi",
  description: "Tortlar va desertlar",
  owner_telegram_username: null,
  city: "Toshkent",
  logo_url: null,
  banner_url: null,
  subscription_type: "free",
  is_featured: false,
};

const img = (seed: string) =>
  `https://picsum.photos/seed/${encodeURIComponent(seed)}/600/750`;

export type DemoFlags = { hot?: boolean; recommended?: boolean; top?: boolean };

type Row = { product: Product; flags: DemoFlags };

const ROWS: Row[] = [
  {
    product: {
      id: "demo-p-01",
      name: "Atirgul buketi «Sevgi»",
      description: "25 ta atirgul, premium qadoq.",
      price: 189000,
      image_url: img("gz-rose-1"),
      category: "Gullar",
      shop_id: DEMO_SHOP_FLOWERS.id,
      is_active: true,
      shops: DEMO_SHOP_FLOWERS,
    },
    flags: { hot: true, top: true },
  },
  {
    product: {
      id: "demo-p-02",
      name: "Sovg‘a qutisi Premium",
      description: "Shokolad, choy va qaymoq.",
      price: 245000,
      image_url: img("gz-box-1"),
      category: "Sovg‘a setlari",
      shop_id: DEMO_SHOP_GIFT.id,
      is_active: true,
      shops: DEMO_SHOP_GIFT,
    },
    flags: { recommended: true },
  },
  {
    product: {
      id: "demo-p-03",
      name: "Tort «Tug‘ilgan kun» 1 kg",
      description: "Yumshoq krem, mevali bezak.",
      price: 320000,
      image_url: img("gz-cake-1"),
      category: "Tug‘ilgan kun",
      shop_id: DEMO_SHOP_SWEET.id,
      is_active: true,
      shops: DEMO_SHOP_SWEET,
    },
    flags: { hot: true },
  },
  {
    product: {
      id: "demo-p-04",
      name: "Ayiqcha gigant",
      description: "80 sm, yumshoq mato.",
      price: 156000,
      image_url: img("gz-bear-1"),
      category: "O‘yinchoqlar",
      shop_id: DEMO_SHOP_GIFT.id,
      is_active: true,
      shops: DEMO_SHOP_GIFT,
    },
    flags: { recommended: true },
  },
  {
    product: {
      id: "demo-p-05",
      name: "Orxideya o‘simligi",
      description: "Idish bilan birga.",
      price: 98000,
      image_url: img("gz-orchid-1"),
      category: "Gullar",
      shop_id: DEMO_SHOP_FLOWERS.id,
      is_active: true,
      shops: DEMO_SHOP_FLOWERS,
    },
    flags: {},
  },
  {
    product: {
      id: "demo-p-06",
      name: "Sovg‘a kartochkasi + gul",
      description: "Shaxsiy matn yozish mumkin.",
      price: 45000,
      image_url: img("gz-card-1"),
      category: "Sovg‘a setlari",
      shop_id: DEMO_SHOP_GIFT.id,
      is_active: true,
      shops: DEMO_SHOP_GIFT,
    },
    flags: {},
  },
  {
    product: {
      id: "demo-p-07",
      name: "Karamel tort 2 kg",
      description: "24 kishilik.",
      price: 410000,
      image_url: img("gz-cake-2"),
      category: "Tug‘ilgan kun",
      shop_id: DEMO_SHOP_SWEET.id,
      is_active: true,
      shops: DEMO_SHOP_SWEET,
    },
    flags: { top: true },
  },
  {
    product: {
      id: "demo-p-08",
      name: "Qizil atirgul 15 ta",
      description: "Romantik buket.",
      price: 120000,
      image_url: img("gz-rose-2"),
      category: "Gullar",
      shop_id: DEMO_SHOP_FLOWERS.id,
      is_active: true,
      shops: DEMO_SHOP_FLOWERS,
    },
    flags: { hot: true },
  },
  {
    product: {
      id: "demo-p-09",
      name: "Sovg‘a yoritqichi LED",
      description: "Issiq yorug‘lik.",
      price: 89000,
      image_url: img("gz-led-1"),
      category: "Uy bezaklari",
      shop_id: DEMO_SHOP_GIFT.id,
      is_active: true,
      shops: DEMO_SHOP_GIFT,
    },
    flags: {},
  },
  {
    product: {
      id: "demo-p-10",
      name: "Makaron assorti",
      description: "12 dona, quti ichida.",
      price: 75000,
      image_url: img("gz-mac-1"),
      category: "Shirinlik",
      shop_id: DEMO_SHOP_SWEET.id,
      is_active: true,
      shops: DEMO_SHOP_SWEET,
    },
    flags: {},
  },
  {
    product: {
      id: "demo-p-11",
      name: "Tug‘ilgan kun shamollari",
      description: "To‘plam 20 ta.",
      price: 35000,
      image_url: img("gz-ball-1"),
      category: "Tug‘ilgan kun",
      shop_id: DEMO_SHOP_GIFT.id,
      is_active: true,
      shops: DEMO_SHOP_GIFT,
    },
    flags: {},
  },
  {
    product: {
      id: "demo-p-12",
      name: "VIP gul archasi",
      description: "Tadbirlar uchun.",
      price: 520000,
      image_url: img("gz-arch-1"),
      category: "Gullar",
      shop_id: DEMO_SHOP_FLOWERS.id,
      is_active: true,
      shops: DEMO_SHOP_FLOWERS,
    },
    flags: { recommended: true, top: true },
  },
  {
    product: {
      id: "demo-p-13",
      name: "Shokoladlar to‘plami",
      description: "Belgiya shokoladi.",
      price: 198000,
      image_url: img("gz-choc-1"),
      category: "Sovg‘a setlari",
      shop_id: DEMO_SHOP_GIFT.id,
      is_active: true,
      shops: DEMO_SHOP_GIFT,
    },
    flags: {},
  },
  {
    product: {
      id: "demo-p-14",
      name: "Kichik tort «Yulduz»",
      description: "4-6 kishi.",
      price: 165000,
      image_url: img("gz-cake-3"),
      category: "Tug‘ilgan kun",
      shop_id: DEMO_SHOP_SWEET.id,
      is_active: true,
      shops: DEMO_SHOP_SWEET,
    },
    flags: {},
  },
  {
    product: {
      id: "demo-p-15",
      name: "Pushti lola buketi",
      description: "Yoqimli hid.",
      price: 134000,
      image_url: img("gz-tulip-1"),
      category: "Gullar",
      shop_id: DEMO_SHOP_FLOWERS.id,
      is_active: true,
      shops: DEMO_SHOP_FLOWERS,
    },
    flags: { hot: true },
  },
];

export const MOCK_PRODUCTS: Product[] = ROWS.map((r) => r.product);

export const MOCK_SHOPS: Shop[] = [
  DEMO_SHOP_GIFT,
  DEMO_SHOP_FLOWERS,
  DEMO_SHOP_SWEET,
];

export function getDemoShopById(id: string): Shop | null {
  return MOCK_SHOPS.find((s) => s.id === id) ?? null;
}

export function mergeShopsWithMock(real: Shop[], min: number): Shop[] {
  const out = [...real];
  const seen = new Set(out.map((s) => s.id));
  for (const m of MOCK_SHOPS) {
    if (out.length >= min) break;
    if (!seen.has(m.id)) {
      out.push(m);
      seen.add(m.id);
    }
  }
  return out;
}

const flagsById = new Map<string, DemoFlags>(
  ROWS.map((r) => [r.product.id, r.flags])
);

export function getDemoFlagsForProduct(id: string): DemoFlags {
  return flagsById.get(id) ?? {};
}

export function getDemoProductById(id: string): Product | null {
  return ROWS.find((r) => r.product.id === id)?.product ?? null;
}

export function mockProductsHot(): Product[] {
  return ROWS.filter((r) => r.flags.hot).map((r) => r.product);
}

export function mockProductsRecommended(): Product[] {
  return ROWS.filter((r) => r.flags.recommended).map((r) => r.product);
}

export function mockProductsBirthday(): Product[] {
  return ROWS.filter(
    (r) =>
      (r.product.category &&
        /tug['']ilgan|bayram|tort|kun/i.test(r.product.category)) ||
      /tort|tug['']ilgan|sham/i.test(
        (r.product.name + " " + (r.product.description ?? "")).toLowerCase()
      )
  ).map((r) => r.product);
}

export function mergeWithMock(
  real: Product[],
  min: number,
  mockPool: Product[]
): Product[] {
  const out: Product[] = [...real];
  const seen = new Set(out.map((p) => p.id));
  for (const m of mockPool) {
    if (out.length >= min) break;
    if (!seen.has(m.id)) {
      out.push(m);
      seen.add(m.id);
    }
  }
  for (const m of MOCK_PRODUCTS) {
    if (out.length >= min) break;
    if (!seen.has(m.id)) {
      out.push(m);
      seen.add(m.id);
    }
  }
  return out;
}

export function pickBirthdayFromList(list: Product[]): Product[] {
  return list.filter(
    (x) =>
      (x.category && /tug['']ilgan|bayram|tort|kun/i.test(x.category)) ||
      /tort|tug['']ilgan|bayram|kun|sham/i.test(
        (x.name + " " + (x.description ?? "")).toLowerCase()
      )
  );
}

export function sortByShopPremium(a: Product, b: Product): number {
  const tier = (s: Product["shops"]) => {
    const t = s?.subscription_type;
    if (t === "vip") return 0;
    if (t === "pro") return 1;
    return 2;
  };
  const ta = tier(a.shops);
  const tb = tier(b.shops);
  if (ta !== tb) return ta - tb;
  const fa = a.shops?.is_featured ? 0 : 1;
  const fb = b.shops?.is_featured ? 0 : 1;
  if (fa !== fb) return fa - fb;
  return 0;
}
