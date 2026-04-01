import { createClient } from "@supabase/supabase-js";
import type { Product, Shop } from "@/types";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

function jwtRoleSegment(key: string): string | undefined {
  try {
    const seg = key.split(".")[1];
    if (!seg) return undefined;
    const b64 = seg.replace(/-/g, "+").replace(/_/g, "/");
    const pad = b64.length % 4 === 0 ? "" : "=".repeat(4 - (b64.length % 4));
    const json = JSON.parse(atob(b64 + pad)) as { role?: string };
    return json.role;
  } catch {
    return undefined;
  }
}

export function getSupabaseBrowserClient() {
  if (!url || !key) {
    throw new Error(
      "Supabase: NEXT_PUBLIC_SUPABASE_URL va NEXT_PUBLIC_SUPABASE_ANON_KEY topilmadi. " +
        "Mahalliy: .env yoki .env.local ga qo‘shing. Vercel: Environment Variables + Redeploy."
    );
  }
  if (jwtRoleSegment(key) === "service_role") {
    throw new Error(
      "Brauzerda service_role (maxfiy) kalit ishlatilmasin. " +
        "Supabase → Settings → API dan «anon» / «public» kalitni nusxalang — " +
        "NEXT_PUBLIC_SUPABASE_ANON_KEY ga shuni qo‘ying (service_role emas)."
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
