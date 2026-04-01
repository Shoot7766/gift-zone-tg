"use client";

import { cn } from "@/lib/utils";

export type SortOption = "latest" | "price_asc" | "price_desc";

const options: { value: SortOption; label: string }[] = [
  { value: "latest", label: "Yangi" },
  { value: "price_asc", label: "Narx ↑" },
  { value: "price_desc", label: "Narx ↓" },
];

type Props = {
  sort: SortOption;
  onSortChange: (s: SortOption) => void;
  className?: string;
};

export function FilterBar({ sort, onSortChange, className }: Props) {
  return (
    <div
      className={cn(
        "flex items-center gap-2 overflow-x-auto pb-1 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden",
        className
      )}
    >
      <span className="shrink-0 text-xs font-medium text-muted-foreground">
        Tartib:
      </span>
      {options.map((o) => (
        <button
          key={o.value}
          type="button"
          onClick={() => onSortChange(o.value)}
          className={cn(
            "shrink-0 rounded-lg border px-3 py-1.5 text-xs font-semibold transition-all",
            sort === o.value
              ? "border-amber-500/50 bg-amber-500/10 text-foreground"
              : "border-transparent bg-muted/60 text-muted-foreground hover:bg-muted"
          )}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}
