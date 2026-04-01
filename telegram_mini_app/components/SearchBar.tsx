"use client";

import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

type Props = {
  value: string;
  onChange: (v: string) => void;
  onSubmit?: () => void;
  placeholder?: string;
  className?: string;
};

export function SearchBar({
  value,
  onChange,
  onSubmit,
  placeholder = "Sovg'a yoki mahsulot qidiring…",
  className,
}: Props) {
  return (
    <div className={cn("relative", className)}>
      <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
      <Input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onSubmit?.()}
        placeholder={placeholder}
        className="h-12 border-border/60 bg-card/90 pl-11 pr-4 shadow-soft"
      />
    </div>
  );
}
