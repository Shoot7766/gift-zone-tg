"use client";

import Link from "next/link";
import type { Product } from "@/types";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatPriceUZS } from "@/lib/utils";
import { ProductImage } from "@/components/ProductImage";
import { Store } from "lucide-react";

type Props = { product: Product; className?: string };

export function ProductCard({ product, className }: Props) {
  const shop = product.shops;
  const featured = shop?.is_featured;
  const vip = shop?.subscription_type === "vip";

  return (
    <Link href={`/products/${product.id}`} className={className}>
      <Card className="group overflow-hidden border-border/50 transition-all duration-300 hover:border-amber-500/30 hover:shadow-glow active:scale-[0.99]">
        <div className="relative aspect-[4/3] w-full">
          <ProductImage
            src={product.image_url}
            alt={product.name}
            className="h-full w-full rounded-none"
          />
          <div className="absolute right-2 top-2 flex flex-wrap justify-end gap-1">
            {vip && (
              <Badge variant="vip" className="backdrop-blur-sm">
                Top
              </Badge>
            )}
            {featured && (
              <Badge variant="accent" className="backdrop-blur-sm">
                Tavsiya
              </Badge>
            )}
          </div>
        </div>
        <CardContent className="space-y-2 p-4">
          <p className="line-clamp-2 font-display text-base font-semibold leading-snug group-hover:text-amber-800 dark:group-hover:text-amber-200">
            {product.name}
          </p>
          <p className="text-lg font-bold text-amber-700 dark:text-amber-400">
            {formatPriceUZS(product.price)}
          </p>
          {shop && (
            <p className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <Store className="h-3.5 w-3.5 shrink-0" />
              <span className="truncate">{shop.name}</span>
            </p>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}
