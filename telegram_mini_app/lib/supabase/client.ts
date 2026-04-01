import { createClient } from "@supabase/supabase-js";
import type { Product, Shop } from "@/types";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export function getSupabaseBrowserClient() {
  if (!url || !key) {
    throw new Error(
      "Supabase: NEXT_PUBLIC_SUPABASE_URL va NEXT_PUBLIC_SUPABASE_ANON_KEY topilmadi. " +
        "Mahalliy: .env yoki .env.local ga qo‘shing. Vercel: Environment Variables + Redeploy."
    );
  }
  return createClient(url, key);
}

type ProductRow = Product & { shops?: Shop | Shop[] | null };

function normalizeShop(s: Shop | Shop[] | null | undefined): Shop | null {
  if (!s) return null;
  if (Array.isArray(s)) return s[0] ?? null;
  return s;
}

export function mapProductRow(row: ProductRow): Product {
  return {
    ...row,
    shops: normalizeShop(row.shops),
  };
}
