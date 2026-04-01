"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { SearchBar } from "@/components/SearchBar";
import { CategoryChips } from "@/components/CategoryChips";
import { ProductCard } from "@/components/ProductCard";
import { FilterBar, type SortOption } from "@/components/FilterBar";
import { EmptyState } from "@/components/EmptyState";
import { Skeleton } from "@/components/ui/skeleton";
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
        <SearchBar value={q} onChange={setQ} placeholder="Qidiruv…" />
        <CategoryChips
          categories={cats}
          active={activeCat}
          onSelect={setActiveCat}
        />
        <FilterBar sort={sort} onSortChange={setSort} />
        <p className="text-xs text-muted-foreground">
          {loading ? "Yuklanmoqda…" : `Jami: ${list.length} ta natija`}
        </p>
        {loading ? (
          <div className="grid grid-cols-2 gap-3">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <Skeleton key={i} className="aspect-[4/5] rounded-2xl" />
            ))}
          </div>
        ) : list.length === 0 ? (
          <EmptyState
            icon={PackageOpen}
            title="Mahsulot topilmadi"
            description="Boshqa kategoriya yoki kalit so'z bilan qidirib ko'ring."
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
