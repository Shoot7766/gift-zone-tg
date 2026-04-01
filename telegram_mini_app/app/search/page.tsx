"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { SearchBar } from "@/components/SearchBar";
import { CategoryChips } from "@/components/CategoryChips";
import { ProductCard } from "@/components/ProductCard";
import { EmptyState } from "@/components/EmptyState";
import { Skeleton } from "@/components/ui/skeleton";
import { fetchCategories, fetchProducts } from "@/lib/supabase/queries";
import type { Product } from "@/types";
import { Search } from "lucide-react";

function SearchInner() {
  const sp = useSearchParams();
  const initial = sp.get("q") ?? "";
  const [q, setQ] = useState(initial);
  const [cats, setCats] = useState<string[]>([]);
  const [cat, setCat] = useState<string | null>(null);
  const [list, setList] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCategories().then(setCats).catch(() => setCats([]));
  }, []);

  useEffect(() => {
    setQ(initial);
  }, [initial]);

  useEffect(() => {
    let live = true;
    if (!q.trim() && !cat) {
      setList([]);
      return;
    }
    setLoading(true);
    fetchProducts({
      search: q.trim() || null,
      category: cat,
      sort: "latest",
      limit: 60,
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
  }, [q, cat]);

  return (
    <>
      <AppHeader title="Qidiruv" showBack backHref="/" />
      <main className="mx-auto max-w-lg space-y-5 px-4 pb-8 pt-4">
        <SearchBar
          value={q}
          onChange={setQ}
          placeholder="Masalan: gul, sovg'a, tort…"
        />
        <CategoryChips categories={cats} active={cat} onSelect={setCat} />
        {!q.trim() && !cat ? (
          <EmptyState
            icon={Search}
            title="Qidiruvni boshlang"
            description="Yuqorida yozing yoki kategoriya tanlang."
          />
        ) : loading ? (
          <div className="grid grid-cols-2 gap-3">
            {[1, 2, 3, 4].map((i) => (
              <Skeleton key={i} className="aspect-[4/5] rounded-2xl" />
            ))}
          </div>
        ) : list.length === 0 ? (
          <EmptyState
            icon={Search}
            title="Hech narsa topilmadi"
            description="Boshqa so'z yoki kategoriya bilan urinib ko'ring."
          />
        ) : (
          <>
            <p className="text-xs text-muted-foreground">
              {list.length} ta natija
            </p>
            <div className="grid grid-cols-2 gap-3">
              {list.map((p) => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          </>
        )}
      </main>
    </>
  );
}

export default function SearchPage() {
  return (
    <Suspense
      fallback={
        <>
          <AppHeader title="Qidiruv" showBack />
          <div className="p-4">
            <Skeleton className="h-12 w-full rounded-xl" />
          </div>
        </>
      }
    >
      <SearchInner />
    </Suspense>
  );
}
