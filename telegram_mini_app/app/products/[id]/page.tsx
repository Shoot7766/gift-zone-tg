"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { AppHeader } from "@/components/AppHeader";
import { ProductImage } from "@/components/ProductImage";
import { ProductCard } from "@/components/ProductCard";
import { SellerContactButton } from "@/components/SellerContactButton";
import { FavoriteButton } from "@/components/FavoriteButton";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { formatPriceUZS } from "@/lib/utils";
import {
  fetchProductById,
  fetchRelatedProducts,
} from "@/lib/supabase/queries";
import type { Product } from "@/types";
import { Store } from "lucide-react";

export default function ProductDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [product, setProduct] = useState<Product | null>(null);
  const [related, setRelated] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let ok = true;
    (async () => {
      try {
        const p = await fetchProductById(id);
        if (!ok) return;
        setProduct(p);
        if (p) {
          const r = await fetchRelatedProducts(p, 6);
          if (ok) setRelated(r);
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
        <AppHeader title="Mahsulot" showBack backHref="/products" />
        <div className="p-4 space-y-4">
          <Skeleton className="aspect-square w-full rounded-3xl" />
          <Skeleton className="h-8 w-2/3" />
          <Skeleton className="h-24 w-full" />
        </div>
      </>
    );
  }

  if (!product) {
    return (
      <>
        <AppHeader title="Topilmadi" showBack backHref="/products" />
        <p className="p-6 text-center text-muted-foreground">
          Bu mahsulot mavjud emas yoki o‘chirilgan.
        </p>
      </>
    );
  }

  const shop = product.shops;

  return (
    <>
      <AppHeader title="Mahsulot" showBack backHref="/products" />
      <main className="mx-auto max-w-lg pb-8">
        <div className="relative aspect-square w-full">
          <ProductImage
            src={product.image_url}
            alt={product.name}
            className="h-full w-full"
            priority
          />
          <div className="absolute right-3 top-3">
            <FavoriteButton productId={product.id} className="bg-card/90 shadow-soft" />
          </div>
        </div>

        <div className="space-y-4 px-4 pt-5">
          <div className="flex flex-wrap gap-2">
            {product.category && (
              <Badge variant="secondary" className="capitalize">
                {product.category}
              </Badge>
            )}
            {shop?.subscription_type === "vip" && (
              <Badge variant="vip">Top do&apos;kon</Badge>
            )}
            {shop?.is_featured && <Badge variant="accent">Tavsiya</Badge>}
          </div>

          <h1 className="font-display text-2xl font-bold leading-tight">
            {product.name}
          </h1>
          <p className="text-2xl font-bold text-amber-700 dark:text-amber-400">
            {formatPriceUZS(product.price)}
          </p>

          <Separator />

          <section>
            <h2 className="mb-2 text-sm font-semibold text-muted-foreground">
              Tavsif
            </h2>
            <p className="text-sm leading-relaxed text-foreground/90">
              {product.description || "Tavsif qo'shilmagan."}
            </p>
          </section>

          {shop && (
            <section className="rounded-2xl border border-border/60 bg-card/50 p-4 shadow-inner">
              <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold">
                <Store className="h-4 w-4" />
                Do&apos;kon
              </h2>
              <Link
                href={`/shops/${shop.id}`}
                className="font-display text-lg font-semibold text-amber-800 underline-offset-4 hover:underline dark:text-amber-300"
              >
                {shop.name}
              </Link>
              {shop.city && (
                <p className="mt-1 text-xs text-muted-foreground">{shop.city}</p>
              )}
              <div className="mt-4">
                <SellerContactButton
                  username={shop.owner_telegram_username}
                  size="lg"
                  className="w-full rounded-2xl"
                />
              </div>
            </section>
          )}

          {related.length > 0 && (
            <section className="pt-4">
              <h2 className="mb-3 font-display text-lg font-semibold">
                O&apos;xshash mahsulotlar
              </h2>
              <div className="grid grid-cols-2 gap-3">
                {related.map((p) => (
                  <ProductCard key={p.id} product={p} />
                ))}
              </div>
            </section>
          )}
        </div>
      </main>
    </>
  );
}
