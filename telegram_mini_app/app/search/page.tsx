"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { SearchBar } from "@/components/SearchBar";
import { CategoryChips } from "@/components/CategoryChips";
import { ProductCard } from "@/components/ProductCard";
import { EmptyState } from "@/components/EmptyState";
import { ProductGridSkeleton } from "@/components/ProductGridSkeleton";
import { Skeleton } from "@/components/ui/skeleton";
import { fetchCategories, fetchProducts } from "@/lib/supabase/queries";
import type { Product } from "@/types";
import { Search } from "lucide-react";
import { cn } from "@/lib/utils";

const QUICK_SUGGESTIONS = ["gullar", "ayiqcha", "sovg‘a box", "tort"] as const;

function SearchInner() {
  const router = useRouter();
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

  const submitSearch = () => {
    const s = q.trim();
    if (s) router.push(`/search?q=${encodeURIComponent(s)}`);
  };

  const pickSuggestion = (word: string) => {
    setQ(word);
    router.push(`/search?q=${encodeURIComponent(word)}`);
  };

  return (
    <>
      <AppHeader title="Qidiruv" showBack backHref="/" />
      <main className="mx-auto max-w-lg space-y-5 px-4 pb-8 pt-4">
        <SearchBar
          value={q}
          onChange={setQ}
          onSubmit={submitSearch}
          placeholder="Masalan: qizga sovg‘a"
        />

        <div>
          <p className="mb-2 text-xs font-semibold text-muted-foreground">
            Tez takliflar
          </p>
          <div className="flex flex-wrap gap-2">
            {QUICK_SUGGESTIONS.map((word) => (
              <button
                key={word}
                type="button"
                onClick={() => pickSuggestion(word)}
                className={cn(
                  "rounded-full border border-border/80 bg-card px-3 py-1.5 text-xs font-semibold text-foreground shadow-sm",
                  "transition-colors hover:border-amber-500/40 hover:bg-amber-500/10"
                )}
              >
                {word}
              </button>
            ))}
          </div>
        </div>

        <CategoryChips categories={cats} active={cat} onSelect={setCat} />

        {!q.trim() && !cat ? (
          <EmptyState
            icon={Search}
            title="Qidiruvni boshlang"
            description="Yuqorida yozing, tez taklifni tanlang yoki kategoriya bosing."
          />
        ) : loading ? (
          <ProductGridSkeleton count={6} />
        ) : list.length === 0 ? (
          <EmptyState
            icon={Search}
            title="Hech narsa topilmadi"
            description="Boshqa so‘z yoki kategoriya bilan urinib ko‘ring."
          />
        ) : (
          <>
            <p className="text-sm font-semibold text-foreground">
              {list.length} ta natija topildi
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
            <Skeleton className="h-12 w-full rounded-2xl" />
          </div>
        </>
      }
    >
      <SearchInner />
    </Suspense>
  );
}
