"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { SearchBar } from "@/components/SearchBar";
import { CategoryChips } from "@/components/CategoryChips";
import { ProductCard } from "@/components/ProductCard";
import { ShopCard } from "@/components/ShopCard";
import { FeaturedBanner } from "@/components/FeaturedBanner";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import {
  fetchCategories,
  fetchFeaturedProducts,
  fetchFeaturedShops,
} from "@/lib/supabase/queries";
import { useTelegramUser } from "@/lib/telegram";
import type { Product, Shop } from "@/types";
import { ArrowRight } from "lucide-react";

export default function HomePage() {
  const router = useRouter();
  const { user } = useTelegramUser();
  const [q, setQ] = useState("");
  const [cats, setCats] = useState<string[]>([]);
  const [cat, setCat] = useState<string | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [shops, setShops] = useState<Shop[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let ok = true;
    (async () => {
      try {
        const [c, p, s] = await Promise.all([
          fetchCategories(),
          fetchFeaturedProducts(8),
          fetchFeaturedShops(4),
        ]);
        if (!ok) return;
        setCats(c);
        setProducts(p);
        setShops(s);
      } catch (e) {
        if (!ok) return;
        setErr(
          e instanceof Error
            ? e.message
            : "Ma'lumot yuklanmadi. .env va Supabase RLS ni tekshiring."
        );
      } finally {
        if (ok) setLoading(false);
      }
    })();
    return () => {
      ok = false;
    };
  }, []);

  const greeting = user?.first_name
    ? `Salom, ${user.first_name}`
    : "Xush kelibsiz";

  return (
    <>
      <AppHeader title="Gift Zone" />
      <main className="mx-auto max-w-lg space-y-8 px-4 pb-8 pt-4">
        <section className="space-y-2">
          <p className="text-sm font-medium text-amber-700 dark:text-amber-400">
            {greeting}
          </p>
          <h2 className="font-display text-2xl font-bold leading-tight text-foreground">
            Bugun nimani izlayapsiz?
          </h2>
          <p className="text-sm text-muted-foreground">
            Eng yaxshi do&apos;konlardan tanlangan mahsulotlar — barchasi Telegram
            ichida.
          </p>
        </section>

        <SearchBar
          value={q}
          onChange={setQ}
          onSubmit={() => {
            const s = q.trim();
            if (s) router.push(`/search?q=${encodeURIComponent(s)}`);
          }}
        />

        {err && (
          <p className="rounded-xl border border-destructive/30 bg-destructive/5 p-4 text-sm text-destructive">
            {err}
          </p>
        )}

        <FeaturedBanner />

        <section className="space-y-3">
          <div className="flex items-end justify-between">
            <h3 className="font-display text-lg font-semibold">Kategoriyalar</h3>
            <Button variant="ghost" size="sm" className="h-8 text-xs" asChild>
              <Link href="/products">Barchasi</Link>
            </Button>
          </div>
          {loading ? (
            <Skeleton className="h-10 w-full" />
          ) : (
            <CategoryChips
              categories={cats}
              active={cat}
              onSelect={(c) => {
                setCat(c);
                const params = new URLSearchParams();
                if (c) params.set("category", c);
                router.push(`/products?${params.toString()}`);
              }}
            />
          )}
        </section>

        <section className="space-y-4">
          <div className="flex items-end justify-between">
            <h3 className="font-display text-lg font-semibold">
              Tavsiya etilganlar
            </h3>
            <Link
              href="/products"
              className="flex items-center gap-1 text-xs font-semibold text-amber-700 dark:text-amber-400"
            >
              Ko&apos;rish
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
          {loading ? (
            <div className="grid grid-cols-2 gap-3">
              {[1, 2, 3, 4].map((i) => (
                <Skeleton key={i} className="aspect-[4/5] rounded-2xl" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {products.map((p) => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          )}
        </section>

        <section className="space-y-4">
          <div className="flex items-end justify-between">
            <h3 className="font-display text-lg font-semibold">Top do&apos;konlar</h3>
            <Link
              href="/shops"
              className="flex items-center gap-1 text-xs font-semibold text-amber-700 dark:text-amber-400"
            >
              Barcha do&apos;konlar
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
          {loading ? (
            <div className="space-y-3">
              <Skeleton className="h-28 rounded-2xl" />
              <Skeleton className="h-28 rounded-2xl" />
            </div>
          ) : (
            <div className="space-y-3">
              {shops.map((s) => (
                <ShopCard key={s.id} shop={s} />
              ))}
            </div>
          )}
        </section>
      </main>
    </>
  );
}
