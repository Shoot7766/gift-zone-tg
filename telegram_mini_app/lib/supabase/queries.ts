import type { Product, Shop } from "@/types";
import { getSupabaseBrowserClient, mapProductRow } from "./client";

const productSelect = `
  id, name, description, price, image_url, category, shop_id, is_active, created_at,
  shops (
    id, name, description, owner_telegram_username, city,
    logo_url, banner_url, subscription_type, is_featured
  )
`;

function shopSortKey(s: Shop): [number, number, string] {
  const tier = s.subscription_type === "vip" ? 0 : s.subscription_type === "pro" ? 1 : 2;
  const feat = s.is_featured ? 0 : 1;
  return [tier, feat, s.created_at ?? ""];
}

export async function fetchFeaturedShops(limit = 6): Promise<Shop[]> {
  const sb = getSupabaseBrowserClient();
  const { data, error } = await sb.from("shops").select("*").limit(limit * 2);
  if (error) throw error;
  const rows = (data ?? []) as Shop[];
  return rows.sort((a, b) => {
    const ka = shopSortKey(a);
    const kb = shopSortKey(b);
    for (let i = 0; i < 3; i++) {
      if (ka[i] !== kb[i]) return ka[i] < kb[i] ? -1 : 1;
    }
    return 0;
  }).slice(0, limit);
}

export async function fetchShops(): Promise<Shop[]> {
  const sb = getSupabaseBrowserClient();
  const { data, error } = await sb.from("shops").select("*");
  if (error) throw error;
  const rows = (data ?? []) as Shop[];
  return rows.sort((a, b) => {
    const ka = shopSortKey(a);
    const kb = shopSortKey(b);
    for (let i = 0; i < 3; i++) {
      if (ka[i] !== kb[i]) return ka[i] < kb[i] ? -1 : 1;
    }
    return 0;
  });
}

export async function fetchShopById(id: string): Promise<Shop | null> {
  const sb = getSupabaseBrowserClient();
  const { data, error } = await sb.from("shops").select("*").eq("id", id).maybeSingle();
  if (error) throw error;
  return (data as Shop) ?? null;
}

export async function fetchProductsByShop(shopId: string): Promise<Product[]> {
  const sb = getSupabaseBrowserClient();
  const { data, error } = await sb
    .from("products")
    .select(productSelect)
    .eq("shop_id", shopId)
    .eq("is_active", true)
    .order("created_at", { ascending: false });
  if (error) throw error;
  return (data ?? []).map((r) => mapProductRow(r as Parameters<typeof mapProductRow>[0]));
}

export async function fetchFeaturedProducts(limit = 8): Promise<Product[]> {
  const sb = getSupabaseBrowserClient();
  const { data, error } = await sb
    .from("products")
    .select(productSelect)
    .eq("is_active", true)
    .order("created_at", { ascending: false })
    .limit(limit * 2);
  if (error) throw error;
  const products = (data ?? []).map((r) => mapProductRow(r as Parameters<typeof mapProductRow>[0]));
  products.sort((a, b) => {
    const sa = a.shops;
    const sb_ = b.shops;
    if (!sa || !sb_) return 0;
    const ka = shopSortKey(sa);
    const kb = shopSortKey(sb_);
    for (let i = 0; i < 3; i++) {
      if (ka[i] !== kb[i]) return ka[i] < kb[i] ? -1 : 1;
    }
    return 0;
  });
  return products.slice(0, limit);
}

export async function fetchProducts(options?: {
  category?: string | null;
  search?: string | null;
  sort?: "latest" | "price_asc" | "price_desc";
  limit?: number;
}): Promise<Product[]> {
  const sb = getSupabaseBrowserClient();
  let q = sb.from("products").select(productSelect).eq("is_active", true);

  if (options?.category) {
    q = q.ilike("category", `%${options.category}%`);
  }
  if (options?.search?.trim()) {
    const raw = options.search.trim().replace(/%/g, "").replace(/,/g, " ");
    const t = `%${raw}%`;
    q = q.or(
      `name.ilike.${t},description.ilike.${t},keywords.ilike.${t}`
    );
  }

  const sort = options?.sort ?? "latest";
  if (sort === "price_asc") q = q.order("price", { ascending: true, nullsFirst: false });
  else if (sort === "price_desc") q = q.order("price", { ascending: false, nullsFirst: false });
  else q = q.order("created_at", { ascending: false });

  const lim = options?.limit ?? 60;
  const { data, error } = await q.limit(lim);
  if (error) throw error;
  const products = (data ?? []).map((r) => mapProductRow(r as Parameters<typeof mapProductRow>[0]));
  products.sort((a, b) => {
    const sa = a.shops;
    const sb_ = b.shops;
    if (!sa || !sb_) return 0;
    const ka = shopSortKey(sa);
    const kb = shopSortKey(sb_);
    for (let i = 0; i < 3; i++) {
      if (ka[i] !== kb[i]) return ka[i] < kb[i] ? -1 : 1;
    }
    return 0;
  });
  return products;
}

export async function fetchProductById(id: string): Promise<Product | null> {
  const sb = getSupabaseBrowserClient();
  const { data, error } = await sb
    .from("products")
    .select(productSelect)
    .eq("id", id)
    .eq("is_active", true)
    .maybeSingle();
  if (error) throw error;
  if (!data) return null;
  return mapProductRow(data as Parameters<typeof mapProductRow>[0]);
}

export async function fetchRelatedProducts(
  product: Product,
  limit = 6
): Promise<Product[]> {
  const sb = getSupabaseBrowserClient();
  const { shop_id, category, id } = product;
  const { data, error } = await sb
    .from("products")
    .select(productSelect)
    .eq("is_active", true)
    .eq("shop_id", shop_id)
    .neq("id", id)
    .limit(limit + 4);
  if (error) throw error;
  let list = (data ?? []).map((r) => mapProductRow(r as Parameters<typeof mapProductRow>[0]));
  if (category?.trim()) {
    const catLower = category.trim().toLowerCase();
    const sameCat = list.filter(
      (p) => p.category?.toLowerCase().includes(catLower)
    );
    const other = list.filter(
      (p) => !p.category?.toLowerCase().includes(catLower)
    );
    list = [...sameCat, ...other];
  }
  list = list.slice(0, limit);
  if (list.length < limit) {
    const rest = await fetchProducts({ limit: 20 });
    for (const p of rest) {
      if (p.id === id || list.some((x) => x.id === p.id)) continue;
      list.push(p);
      if (list.length >= limit) break;
    }
  }
  return list.slice(0, limit);
}

export async function fetchCategories(): Promise<string[]> {
  const sb = getSupabaseBrowserClient();
  const { data, error } = await sb.from("products").select("category").eq("is_active", true);
  if (error) throw error;
  const set = new Set<string>();
  for (const row of data ?? []) {
    const c = (row as { category: string | null }).category;
    if (c?.trim()) set.add(c.trim());
  }
  return Array.from(set).sort((a, b) => a.localeCompare(b, "uz"));
}

export async function fetchProductsByIds(ids: string[]): Promise<Product[]> {
  if (!ids.length) return [];
  const sb = getSupabaseBrowserClient();
  const { data, error } = await sb
    .from("products")
    .select(productSelect)
    .in("id", ids)
    .eq("is_active", true);
  if (error) throw error;
  const map = new Map(
    (data ?? []).map((r) => {
      const p = mapProductRow(r as Parameters<typeof mapProductRow>[0]);
      return [p.id, p] as const;
    })
  );
  return ids.map((id) => map.get(id)).filter(Boolean) as Product[];
}
