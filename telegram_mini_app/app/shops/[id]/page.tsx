"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { useParams } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { ProductCard } from "@/components/ProductCard";
import { SellerContactButton } from "@/components/SellerContactButton";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  fetchShopById,
  fetchProductsByShop,
} from "@/lib/supabase/queries";
import type { Product, Shop } from "@/types";
import { MapPin } from "lucide-react";
import { cn } from "@/lib/utils";

export default function ShopDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [shop, setShop] = useState<Shop | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let ok = true;
    (async () => {
      try {
        const s = await fetchShopById(id);
        if (!ok) return;
        setShop(s);
        if (s) {
          const p = await fetchProductsByShop(id);
          if (ok) setProducts(p);
        }
      } finally {
        if (ok) setLoading(false);
      }
    })();
    return () => {
      ok = false;
    };
  }, [id]);

  if (loading) {
    return (
      <>
        <AppHeader title="Do'kon" showBack backHref="/shops" />
        <Skeleton className="h-40 w-full" />
        <div className="p-4 space-y-3">
          <Skeleton className="h-10 w-1/2" />
          <Skeleton className="h-20 w-full" />
        </div>
      </>
    );
  }

  if (!shop) {
    return (
      <>
        <AppHeader title="Topilmadi" showBack backHref="/shops" />
        <p className="p-6 text-center text-muted-foreground">Do&apos;kon topilmadi.</p>
      </>
    );
  }

  const vip = shop.subscription_type === "vip";

  return (
    <>
      <AppHeader title={shop.name} showBack backHref="/shops" />
      <main className="mx-auto max-w-lg pb-8">
        <div
          className={cn(
            "relative h-36 w-full overflow-hidden bg-gradient-to-br from-amber-200 via-stone-200 to-stone-400 dark:from-amber-950 dark:via-stone-900 dark:to-stone-950"
          )}
        >
          {shop.banner_url ? (
            <Image
              src={shop.banner_url}
              alt=""
              fill
              className="object-cover"
              priority
              unoptimized
            />
          ) : null}
          <div className="absolute inset-0 bg-gradient-to-t from-background/90 to-transparent" />
        </div>

        <div className="-mt-12 relative flex flex-col items-center px-4">
          <div
            className={cn(
              "flex h-24 w-24 items-center justify-center overflow-hidden rounded-3xl border-4 border-background bg-card shadow-soft"
            )}
          >
            {shop.logo_url ? (
              <Image
                src={shop.logo_url}
                alt={shop.name}
                width={96}
                height={96}
                className="h-full w-full object-cover"
                unoptimized
              />
            ) : (
              <span className="font-display text-3xl font-bold text-amber-700">
                {shop.name.slice(0, 1).toUpperCase()}
              </span>
            )}
          </div>
          <div className="mt-4 flex flex-wrap justify-center gap-2">
            {vip && <Badge variant="vip">Top do&apos;kon</Badge>}
            {shop.is_featured && <Badge variant="accent">Tavsiya</Badge>}
            {shop.subscription_type === "pro" && !vip && (
              <Badge variant="secondary">Pro</Badge>
            )}
          </div>
          <h1 className="mt-2 text-center font-display text-2xl font-bold">
            {shop.name}
          </h1>
          {shop.city && (
            <p className="mt-1 flex items-center gap-1 text-sm text-muted-foreground">
              <MapPin className="h-4 w-4" />
              {shop.city}
            </p>
          )}
          <p className="mt-3 text-center text-sm leading-relaxed text-muted-foreground">
            {shop.description || "Tavsif qo'shilmagan."}
          </p>
          <div className="mt-5 w-full max-w-sm">
            <SellerContactButton
              username={shop.owner_telegram_username}
              size="lg"
              className="w-full rounded-2xl"
            />
          </div>
        </div>

        <div className="mt-10 px-4">
          <h2 className="mb-4 font-display text-lg font-semibold">
            Do&apos;kon mahsulotlari
          </h2>
          {products.length === 0 ? (
            <p className="text-sm text-muted-foreground">Hozircha mahsulot yo&apos;q.</p>
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {products.map((p) => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          )}
        </div>
      </main>
    </>
  );
}
