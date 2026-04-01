"use client";

import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type Props = { className?: string };

export function FeaturedBanner({ className }: Props) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-3xl border border-amber-500/20 bg-gradient-to-br from-amber-500/90 via-amber-600 to-stone-900 p-6 text-stone-50 shadow-glow",
        className
      )}
    >
      <div className="pointer-events-none absolute -right-8 -top-8 h-32 w-32 rounded-full bg-white/10 blur-2xl" />
      <div className="pointer-events-none absolute -bottom-10 left-1/4 h-24 w-48 rounded-full bg-amber-300/20 blur-3xl" />
      <div className="relative z-10 space-y-3">
        <div className="inline-flex items-center gap-2 rounded-full bg-black/20 px-3 py-1 text-xs font-semibold backdrop-blur-sm">
          <Sparkles className="h-3.5 w-3.5" />
          Premium bozor
        </div>
        <h2 className="font-display text-2xl font-bold leading-tight">
          Sovg&apos;a va gul — bir joyda
        </h2>
        <p className="max-w-sm text-sm text-amber-100/90">
          Eng yaxshi do&apos;konlardan tanlangan mahsulotlarni kashf eting. Telegram orqali
          sotuvchi bilan bir zumda bog&apos;laning.
        </p>
        <Button
          asChild
          size="sm"
          className="mt-2 rounded-xl bg-stone-950 text-amber-50 hover:bg-stone-900"
        >
          <Link href="/products" className="gap-2">
            Mahsulotlarni ko&apos;rish
            <ArrowRight className="h-4 w-4" />
          </Link>
        </Button>
      </div>
    </div>
  );
}
