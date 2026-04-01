"use client";

import { useEffect, useState } from "react";
import { Heart } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { isFavoriteId, toggleFavoriteId } from "@/lib/favorites";

type Props = {
  productId: string;
  className?: string;
  /** Kartochkada matnli tugma */
  showLabel?: boolean;
};

export function FavoriteButton({ productId, className, showLabel }: Props) {
  const [on, setOn] = useState(false);

  useEffect(() => {
    setOn(isFavoriteId(productId));
  }, [productId]);

  return (
    <Button
      type="button"
      variant="outline"
      size={showLabel ? "default" : "icon"}
      className={cn(
        "rounded-xl border-2 transition-colors",
        showLabel && "gap-2",
        on && "border-rose-400/60 bg-rose-50 text-rose-600 dark:bg-rose-950/40 dark:text-rose-300",
        className
      )}
      aria-label={on ? "Saqlanganlardan olib tashlash" : "Saqlash"}
      onClick={() => {
        const next = toggleFavoriteId(productId);
        setOn(next);
      }}
    >
      <Heart
        className={cn(showLabel ? "h-4 w-4" : "h-5 w-5", on && "fill-current")}
        strokeWidth={2}
      />
      {showLabel && <span>⭐ Saqlash</span>}
    </Button>
  );
}
