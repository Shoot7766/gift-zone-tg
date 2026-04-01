"use client";

import { useEffect, useState, useCallback } from "react";
import { AppHeader } from "@/components/AppHeader";
import { ProductCard } from "@/components/ProductCard";
import { EmptyState } from "@/components/EmptyState";
import { Button } from "@/components/ui/button";
import { fetchProductsByIds } from "@/lib/supabase/queries";
import { getFavoriteIds } from "@/lib/favorites";
import type { Product } from "@/types";
import { Heart } from "lucide-react";
import Link from "next/link";

export default function FavoritesPage() {
  const [list, setList] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(() => {
    const ids = getFavoriteIds();
    if (!ids.length) {
      setList([]);
      setLoading(false);
      return;
    }
    setLoading(true);
    fetchProductsByIds(ids)
      .then(setList)
      .catch(() => setList([]))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  useEffect(() => {
    const onFocus = () => load();
    window.addEventListener("focus", onFocus);
    return () => window.removeEventListener("focus", onFocus);
  }, [load]);

  return (
    <>
      <AppHeader title="Saqlanganlar" showBack backHref="/" />
      <main className="mx-auto max-w-lg px-4 pb-8 pt-4">
        <p className="mb-4 text-sm text-muted-foreground">
          Tanlangan mahsulotlar qurilmangizda saqlanadi (Telegram ichida).
        </p>
        {loading ? (
          <p className="text-sm text-muted-foreground">Yuklanmoqda…</p>
        ) : list.length === 0 ? (
          <EmptyState
            icon={Heart}
            title={"Hozircha bo'sh"}
            description={
              "Mahsulot kartochkasidagi yurakcha tugmasini bosing — bu yerda ko'rinadi."
            }
            action={
              <Button asChild variant="accent" className="rounded-xl">
                <Link href="/products">{"Mahsulotlarga o'tish"}</Link>
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
