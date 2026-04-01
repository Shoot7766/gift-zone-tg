"use client";

import Link from "next/link";
import { Sparkles, Bot } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type Props = { className?: string };

const AI_SEARCH_Q = "qiz uchun sovg'a";

export function FeaturedBanner({ className }: Props) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-3xl border border-white/20 bg-gradient-to-br from-violet-600 via-amber-500 to-rose-600 p-6 text-white shadow-[0_20px_50px_-15px_rgba(245,158,11,0.45)]",
        className
      )}
    >
      <div className="pointer-events-none absolute -right-12 -top-12 h-40 w-40 rounded-full bg-white/20 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-16 left-0 h-32 w-56 rounded-full bg-black/20 blur-3xl" />
      <div className="pointer-events-none absolute right-1/4 top-1/2 h-24 w-24 rounded-full bg-amber-300/30 blur-2xl" />

      <div className="relative z-10 space-y-4">
        <div className="inline-flex items-center gap-2 rounded-full bg-black/25 px-3 py-1 text-xs font-bold backdrop-blur-md">
          <Sparkles className="h-3.5 w-3.5 text-amber-200" />
          Gift Zone Premium
        </div>
        <h2 className="font-display text-2xl font-bold leading-tight tracking-tight drop-shadow-sm md:text-[1.65rem]">
          🎁 Sovg‘a topishda yordam beramiz
        </h2>
        <p className="max-w-sm text-sm font-medium leading-relaxed text-white/95">
          AI orqali tez va oson toping — minglab guldasta, tort va sovg‘a g‘oyalari.
        </p>
        <div className="flex flex-col gap-2 sm:flex-row sm:flex-wrap">
          <Button
            asChild
            size="lg"
            className="rounded-2xl border-0 bg-stone-950 font-bold text-amber-50 shadow-lg hover:bg-stone-900"
          >
            <Link
              href={`/search?q=${encodeURIComponent(AI_SEARCH_Q)}`}
              className="gap-2"
            >
              <Bot className="h-5 w-5" />
              🤖 AI orqali topish
            </Link>
          </Button>
          <Button
            asChild
            variant="outline"
            size="lg"
            className="rounded-2xl border border-white/35 bg-white/15 font-semibold text-white shadow-none backdrop-blur-md hover:bg-white/25 hover:text-white"
          >
            <Link href="/products">Barcha mahsulotlar</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
