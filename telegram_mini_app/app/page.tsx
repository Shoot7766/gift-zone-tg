"use client";

import { useEffect, useState, useMemo } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { SearchBar } from "@/components/SearchBar";
import { CategoryChips } from "@/components/CategoryChips";
import { ProductCard } from "@/components/ProductCard";
import { ShopCard } from "@/components/ShopCard";
import { FeaturedBanner } from "@/components/FeaturedBanner";
import { ProductGridSkeleton } from "@/components/ProductGridSkeleton";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import {
  fetchCategories,
  fetchProducts,
  fetchFeaturedShops,
} from "@/lib/supabase/queries";
import { supabaseFetchErrorMessage } from "@/lib/supabase/errorMessage";
import {
  mergeWithMock,
  mergeShopsWithMock,
  mockProductsBirthday,
  mockProductsHot,
  mockProductsRecommended,
  pickBirthdayFromList,
  sortByShopPremium,
} from "@/lib/mockCatalog";
import { useTelegramUser } from "@/lib/telegram";
import type { Product, Shop } from "@/types";
import { ArrowRight, Bot } from "lucide-react";

const AI_HINT = "qiz uchun sovg'a";

function SectionTitle({
  emoji,
  title,
  href,
  linkLabel,
}: {
  emoji: string;
  title: string;
  href: string;
  linkLabel: string;
}) {
  return (
    <div className="flex items-end justify-between gap-2">
      <h3 className="font-display text-lg font-bold leading-tight text-foreground">
        <span className="mr-1.5">{emoji}</span>
        {title}
      </h3>
      <Link
        href={href}
        className="flex shrink-0 items-center gap-1 text-xs font-bold text-amber-700 dark:text-amber-400"
      >
        {linkLabel}
        <ArrowRight className="h-3.5 w-3.5" />
      </Link>
    </div>
  );
}

export default function HomePage() {
  const router = useRouter();
  const { user } = useTelegramUser();
  const [q, setQ] = useState("");
  const [cats, setCats] = useState<string[]>([]);
  const [cat, setCat] = useState<string | null>(null);
  const [pool, setPool] = useState<Product[]>([]);
  const [shops, setShops] = useState<Shop[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let ok = true;
    (async () => {
      try {
        const [c, products, s] = await Promise.all([
          fetchCategories(),
          fetchProducts({ limit: 72, sort: "latest" }),
          fetchFeaturedShops(8),
        ]);
        if (!ok) return;
        setCats(c);
        setPool(products);
        setShops(mergeShopsWithMock(s, 4));
      } catch (e) {
        if (!ok) return;
        setErr(supabaseFetchErrorMessage(e));
        setCats([]);
        setPool([]);
        setShops(mergeShopsWithMock([], 4));
      } finally {
        if (ok) setLoading(false);
      }
    })();
    return () => {
      ok = false;
    };
  }, []);

  const hotProducts = useMemo(() => {
    const sorted = [...pool].sort(sortByShopPremium);
    const base = sorted.slice(0, 16);
    return mergeWithMock(base, 4, mockProductsHot()).slice(0, 4);
  }, [pool]);

  const giftProducts = useMemo(() => {
    const giftish = pool.filter((p) =>
      /sovg|gul|quti|buket|set|choco|shokolad|tort|o'yinchoq|ayiq|yoritqich/i.test(
        `${p.name} ${p.category ?? ""}`
      )
    );
    const base = [...giftish].sort(sortByShopPremium).slice(0, 16);
    const merged = mergeWithMock(
      base.length ? base : [...pool].sort(sortByShopPremium).slice(0, 16),
      4,
      mockProductsRecommended()
    );
    return merged.slice(0, 4);
  }, [pool]);

  const birthdayProducts = useMemo(() => {
    const b = pickBirthdayFromList(pool);
    const base = [...b].sort(sortByShopPremium).slice(0, 16);
    const merged = mergeWithMock(
      base.length ? base : [...pool].sort(sortByShopPremium).slice(0, 16),
      4,
      mockProductsBirthday()
    );
    return merged.slice(0, 4);
  }, [pool]);

  const greeting = user?.first_name
    ? `Salom, ${user.first_name}`
    : "Xush kelibsiz";

  return (
    <>
      <AppHeader title="Gift Zone" />
      <main className="mx-auto max-w-lg space-y-8 px-4 pb-8 pt-4">
        <section className="space-y-2">
          <p className="text-sm font-semibold text-amber-700 dark:text-amber-400">
            {greeting}
          </p>
          <h2 className="font-display text-2xl font-bold leading-tight text-foreground">
            Bugun nimani izlayapsiz?
          </h2>
          <p className="text-sm text-muted-foreground">
            Eng yaxshi do‘konlardan tanlangan mahsulotlar — barchasi Telegram
            ichida.
          </p>
        </section>

        <div className="space-y-3">
          <SearchBar
            value={q}
            onChange={setQ}
            onSubmit={() => {
              const s = q.trim();
              if (s) router.push(`/search?q=${encodeURIComponent(s)}`);
            }}
            placeholder="Masalan: qizga sovg‘a"
          />
          <Button
            variant="outline"
            size="sm"
            className="w-full rounded-2xl border-amber-500/30 bg-amber-500/5 font-semibold text-amber-900 dark:text-amber-100"
            asChild
          >
            <Link
              href={`/search?q=${encodeURIComponent(AI_HINT)}`}
              className="gap-2"
            >
              <Bot className="h-4 w-4" />
              🤖 AI orqali sovg‘a topish
            </Link>
          </Button>
        </div>

        {err && (
          <p className="rounded-2xl border border-destructive/30 bg-destructive/5 p-4 text-sm text-destructive">
            {err}
          </p>
        )}

        <FeaturedBanner />

        <section className="space-y-3">
          <div className="flex items-end justify-between">
            <h3 className="font-display text-lg font-bold">Kategoriyalar</h3>
            <Button variant="ghost" size="sm" className="h-8 text-xs" asChild>
              <Link href="/products">Barchasi</Link>
            </Button>
          </div>
          {loading ? (
            <Skeleton className="h-11 w-full rounded-2xl" />
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
          <SectionTitle
            emoji="🔥"
            title="Bugun mashhur"
            href="/products"
            linkLabel="Barchasi"
          />
          {loading ? (
            <ProductGridSkeleton count={4} />
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {hotProducts.map((p, i) => (
                <ProductCard
                  key={p.id}
                  product={p}
                  sectionHighlight="hot"
                  priorityImage={i < 2}
                />
              ))}
            </div>
          )}
        </section>

        <section className="space-y-4">
          <SectionTitle
            emoji="💝"
            title="Tavsiya etilgan sovg‘alar"
            href="/products"
            linkLabel="Ko‘rish"
          />
          {loading ? (
            <ProductGridSkeleton count={4} />
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {giftProducts.map((p, i) => (
                <ProductCard
                  key={p.id}
                  product={p}
                  sectionHighlight="recommended"
                  priorityImage={i < 2}
                />
              ))}
            </div>
          )}
        </section>

        <section className="space-y-4">
          <SectionTitle
            emoji="🎉"
            title="Tug‘ilgan kun uchun"
            href="/products?category=Tug%27ilgan%20kun"
            linkLabel="Yana"
          />
          {loading ? (
            <ProductGridSkeleton count={4} />
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {birthdayProducts.map((p, i) => (
                <ProductCard
                  key={p.id}
                  product={p}
                  sectionHighlight="top"
                  priorityImage={i < 2}
                />
              ))}
            </div>
          )}
        </section>

        <section className="space-y-4">
          <div className="flex items-end justify-between">
            <h3 className="font-display text-lg font-bold">Top do‘konlar</h3>
            <Link
              href="/shops"
              className="flex items-center gap-1 text-xs font-bold text-amber-700 dark:text-amber-400"
            >
              Barcha do‘konlar
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
          {loading ? (
            <div className="space-y-3">
              <Skeleton className="h-40 rounded-2xl" />
              <Skeleton className="h-40 rounded-2xl" />
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
