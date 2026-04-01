"use client";

import { useEffect, useState, Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { SearchBar } from "@/components/SearchBar";
import { CategoryChips } from "@/components/CategoryChips";
import { ProductCard } from "@/components/ProductCard";
import { FilterBar, type SortOption } from "@/components/FilterBar";
import { EmptyState } from "@/components/EmptyState";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { fetchCategories, fetchProducts } from "@/lib/supabase/queries";
import type { Product } from "@/types";
import { PackageOpen } from "lucide-react";

function ProductsInner() {
  const sp = useSearchParams();
  const initialCat = sp.get("category");
  const initialQ = sp.get("q") ?? "";

  const [q, setQ] = useState(initialQ);
  const [cats, setCats] = useState<string[]>([]);
  const [activeCat, setActiveCat] = useState<string | null>(initialCat);
  const [sort, setSort] = useState<SortOption>("latest");
  const [list, setList] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCategories().then(setCats).catch(() => setCats([]));
  }, []);

  useEffect(() => {
    let live = true;
    setLoading(true);
    fetchProducts({
      category: activeCat,
      search: q.trim() || null,
      sort,
      limit: 80,
    })
      .then((data) => {
        if (live) setList(data);
      })
      .catch(() => {
        if (live) setList([]);
      })
      .finally(() => {
        if (live) setLoading(false);
      });
    return () => {
      live = false;
    };
  }, [activeCat, sort, q]);

  return (
    <>
      <AppHeader title="Mahsulotlar" showBack backHref="/" />
      <main className="mx-auto max-w-lg space-y-5 px-4 pb-8 pt-4">
        <SearchBar
          value={q}
          onChange={setQ}
          placeholder="Masalan: qizga sovg‘a"
        />
        <CategoryChips
          categories={cats}
          active={activeCat}
          onSelect={setActiveCat}
        />
        <FilterBar sort={sort} onSortChange={setSort} />
        {!loading && (
          <p className="text-sm font-semibold text-foreground">
            {list.length} ta natija topildi
          </p>
        )}
        {loading ? (
          <div className="grid grid-cols-2 gap-3">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div
                key={i}
                className="overflow-hidden rounded-2xl border border-border/40 bg-card/40"
              >
                <Skeleton className="aspect-[3/4] w-full rounded-none" />
                <div className="space-y-2 p-3">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-1/2" />
                </div>
              </div>
            ))}
          </div>
        ) : list.length === 0 ? (
          <EmptyState
            icon={PackageOpen}
            title="😕 Hozircha mahsulotlar yo‘q"
            description="👉 Bosh sahifadan tanlang yoki qidiruvdan foydalaning."
            action={
              <Button asChild variant="accent" className="rounded-2xl font-bold">
                <Link href="/">Bosh sahifaga</Link>
              </Button>
            }
          />
        ) : (
          <div className="grid grid-cols-2 gap-3">
            {list.map((p) => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        )}
      </main>
    </>
  );
}

export default function ProductsPage() {
  return (
    <Suspense
      fallback={
        <>
          <AppHeader title="Mahsulotlar" showBack />
          <div className="p-4">
            <Skeleton className="h-12 w-full rounded-xl" />
          </div>
        </>
      }
    >
      <ProductsInner />
    </Suspense>
  );
}
