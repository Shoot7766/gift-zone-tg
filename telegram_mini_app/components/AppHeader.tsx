"use client";

import Link from "next/link";
import { ChevronLeft, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { closeMiniApp } from "@/lib/telegram";

type Props = {
  title?: string;
  showBack?: boolean;
  backHref?: string;
  className?: string;
};

export function AppHeader({
  title = "Gift Zone",
  showBack,
  backHref = "/",
  className,
}: Props) {
  return (
    <header
      className={cn(
        "sticky top-0 z-40 border-b border-border/50 bg-background/85 backdrop-blur-xl",
        className
      )}
    >
      <div className="mx-auto flex h-14 max-w-lg items-center justify-between gap-2 px-4">
        <div className="flex min-w-0 flex-1 items-center gap-2">
          {showBack ? (
            <Button variant="ghost" size="icon" className="shrink-0" asChild>
              <Link href={backHref} aria-label="Orqaga">
                <ChevronLeft className="h-5 w-5" />
              </Link>
            </Button>
          ) : (
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-amber-400 to-amber-600 shadow-glow">
              <Sparkles className="h-4 w-4 text-stone-900" />
            </div>
          )}
          <h1 className="truncate font-display text-lg font-semibold tracking-tight">
            {title}
          </h1>
        </div>
        <Button
          type="button"
          variant="outline"
          size="sm"
          className="shrink-0 rounded-xl px-2.5 text-[11px] font-bold sm:text-xs"
          onClick={() => {
            try {
              closeMiniApp();
            } catch {
              window.history.back();
            }
          }}
        >
          ⬅️ Botga qaytish
        </Button>
      </div>
    </header>
  );
}
