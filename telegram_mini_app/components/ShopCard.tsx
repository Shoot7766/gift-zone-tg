"use client";

import Link from "next/link";
import Image from "next/image";
import type { Shop } from "@/types";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { MapPin } from "lucide-react";
import { cn } from "@/lib/utils";

type Props = { shop: Shop; className?: string };

export function ShopCard({ shop, className }: Props) {
  const vip = shop.subscription_type === "vip";
  const pro = shop.subscription_type === "pro";

  return (
    <Link href={`/shops/${shop.id}`} className={className}>
      <Card className="group overflow-hidden border-border/50 transition-all duration-300 hover:border-amber-500/30 hover:shadow-soft active:scale-[0.99]">
        <div className="relative flex h-24 items-center gap-4 bg-gradient-to-r from-stone-100 to-amber-50/80 p-4 dark:from-stone-900 dark:to-amber-950/30">
          {shop.banner_url ? (
            <div className="absolute inset-0">
              <Image
                src={shop.banner_url}
                alt=""
                fill
                className="object-cover opacity-40"
                unoptimized
              />
            </div>
          ) : null}
          <div className="relative z-10 flex w-full items-center gap-4">
            <div
              className={cn(
                "flex h-14 w-14 shrink-0 items-center justify-center overflow-hidden rounded-2xl border-2 border-white/80 bg-card shadow-soft dark:border-stone-700"
              )}
            >
              {shop.logo_url ? (
                <Image
                  src={shop.logo_url}
                  alt={shop.name}
                  width={56}
                  height={56}
                  className="h-full w-full object-cover"
                  unoptimized
                />
              ) : (
                <span className="font-display text-xl font-bold text-amber-700">
                  {shop.name.slice(0, 1).toUpperCase()}
                </span>
              )}
            </div>
            <div className="min-w-0 flex-1">
              <div className="mb-1 flex flex-wrap items-center gap-1">
                {vip && <Badge variant="vip">{"Top do'kon"}</Badge>}
                {pro && !vip && (
                  <Badge variant="secondary">Pro</Badge>
                )}
                {shop.is_featured && (
                  <Badge variant="accent">Tavsiya</Badge>
                )}
              </div>
              <p className="truncate font-display text-base font-semibold">
                {shop.name}
              </p>
              {shop.city && (
                <p className="mt-0.5 flex items-center gap-1 text-xs text-muted-foreground">
                  <MapPin className="h-3 w-3 shrink-0" />
                  {shop.city}
                </p>
              )}
            </div>
          </div>
        </div>
        <CardContent className="p-4 pt-3">
          <p className="line-clamp-2 text-sm text-muted-foreground">
            {shop.description || "Tavsif qo'shilmoqda."}
          </p>
        </CardContent>
      </Card>
    </Link>
  );
}
