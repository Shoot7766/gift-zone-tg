"use client";

import { cn } from "@/lib/utils";

type Props = {
  categories: string[];
  active: string | null;
  onSelect: (c: string | null) => void;
  className?: string;
};

export function CategoryChips({
  categories,
  active,
  onSelect,
  className,
}: Props) {
  return (
    <div
      className={cn(
        "flex gap-2 overflow-x-auto pb-1 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden",
        className
      )}
    >
      <button
        type="button"
        onClick={() => onSelect(null)}
        className={cn(
          "shrink-0 rounded-full border px-4 py-2 text-xs font-semibold transition-all",
          active === null
            ? "border-amber-500/60 bg-gradient-to-r from-amber-400/25 to-amber-600/20 text-foreground shadow-soft"
            : "border-border/80 bg-card text-muted-foreground hover:border-border"
        )}
      >
        Hammasi
      </button>
      {categories.map((c) => (
        <button
          key={c}
          type="button"
          onClick={() => onSelect(c)}
          className={cn(
            "shrink-0 rounded-full border px-4 py-2 text-xs font-semibold capitalize transition-all",
            active === c
              ? "border-amber-500/60 bg-gradient-to-r from-amber-400/25 to-amber-600/20 text-foreground shadow-soft"
              : "border-border/80 bg-card text-muted-foreground hover:border-border"
          )}
        >
          {c}
        </button>
      ))}
    </div>
  );
}
