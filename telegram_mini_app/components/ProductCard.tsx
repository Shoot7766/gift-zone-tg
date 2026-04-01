"use client";

import Link from "next/link";
import type { Product } from "@/types";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatPriceUZS } from "@/lib/utils";
import { ProductImage } from "@/components/ProductImage";
import { FavoriteButton } from "@/components/FavoriteButton";
import { SellerContactButton } from "@/components/SellerContactButton";
import { getDemoFlagsForProduct, type DemoFlags } from "@/lib/mockCatalog";
import { Store } from "lucide-react";
import { cn } from "@/lib/utils";

type Highlight = "hot" | "recommended" | "top";

type Props = {
  product: Product;
  className?: string;
  /** Bo‘limdan keladigan ustunlik (demo + real) */
  sectionHighlight?: Highlight | null;
  priorityImage?: boolean;
};

function pickBadges(
  product: Product,
  demo: DemoFlags,
  section: Highlight | null | undefined
): { label: string; key: string }[] {
  const badges: { label: string; key: string }[] = [];
  if (section === "hot" || demo.hot) badges.push({ label: "🔥 Mashhur", key: "hot" });
  const tavsiya =
    section === "recommended" ||
    demo.recommended ||
    product.shops?.is_featured === true;
  if (tavsiya) badges.push({ label: "⭐ Tavsiya etiladi", key: "rec" });
  const top =
    section === "top" ||
    demo.top ||
    product.shops?.subscription_type === "vip";
  if (top) badges.push({ label: "🔝 Top", key: "top" });
  const seen = new Set<string>();
  return badges
    .filter((b) => {
      if (seen.has(b.key)) return false;
      seen.add(b.key);
      return true;
    })
    .slice(0, 2);
}

export function ProductCard({
  product,
  className,
  sectionHighlight,
  priorityImage,
}: Props) {
  const shop = product.shops;
  const demo = getDemoFlagsForProduct(product.id);
  const badges = pickBadges(product, demo, sectionHighlight ?? null);

  return (
    <Card
      className={cn(
        "group flex h-full flex-col overflow-hidden border-0 bg-card shadow-soft ring-1 ring-black/[0.06] transition-all duration-300 dark:ring-white/10",
        "rounded-2xl hover:-translate-y-0.5 hover:shadow-lg hover:ring-amber-500/25 active:scale-[0.99]",
        className
      )}
    >
      <Link href={`/products/${product.id}`} className="block min-h-0 flex-1">
        <div className="relative aspect-[3/4] w-full overflow-hidden">
          <ProductImage
            src={product.image_url}
            alt={product.name}
            className="h-full w-full"
            priority={priorityImage}
          />
          {badges.length > 0 && (
            <div className="absolute left-2 right-2 top-2 flex flex-wrap gap-1">
              {badges.map((b) => (
                <Badge
                  key={b.key}
                  variant={b.key === "top" ? "vip" : "accent"}
                  className="max-w-[95%] truncate border-0 bg-black/45 text-[10px] font-bold text-white backdrop-blur-md"
                >
                  {b.label}
                </Badge>
              ))}
            </div>
          )}
        </div>
        <div className="space-y-1.5 p-3">
          <p className="line-clamp-2 min-h-[2.5rem] font-display text-sm font-semibold leading-snug text-foreground group-hover:text-amber-800 dark:group-hover:text-amber-200">
            {product.name}
          </p>
          <p className="text-base font-bold tracking-tight text-amber-700 dark:text-amber-400">
            {formatPriceUZS(product.price)}
          </p>
          {shop && (
            <p className="flex items-center gap-1 text-xs text-muted-foreground">
              <Store className="h-3 w-3 shrink-0 opacity-70" />
              <span className="truncate font-medium">{shop.name}</span>
            </p>
          )}
        </div>
      </Link>
      <div className="mt-auto flex flex-col gap-2 border-t border-border/40 px-3 pb-3 pt-2">
        <SellerContactButton
          username={shop?.owner_telegram_username}
          size="default"
          compactLabel
          className="h-9 w-full rounded-xl text-xs font-semibold"
        />
        <FavoriteButton
          productId={product.id}
          showLabel
          className="h-9 w-full rounded-xl border-border/80 text-xs font-semibold"
        />
      </div>
    </Card>
  );
}
