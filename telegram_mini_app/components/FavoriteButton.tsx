"use client";

import { useEffect, useState } from "react";
import { Heart } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { isFavoriteId, toggleFavoriteId } from "@/lib/favorites";

type Props = {
  productId: string;
  className?: string;
};

export function FavoriteButton({ productId, className }: Props) {
  const [on, setOn] = useState(false);

  useEffect(() => {
    setOn(isFavoriteId(productId));
  }, [productId]);

  return (
    <Button
      type="button"
      variant="outline"
      size="icon"
      className={cn(
        "rounded-xl border-2 transition-colors",
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
        className={cn("h-5 w-5", on && "fill-current")}
        strokeWidth={2}
      />
    </Button>
  );
}
