"use client";

import Link from "next/link";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import { Bot, Building2, Package, Sparkles } from "lucide-react";

const botUser = process.env.NEXT_PUBLIC_TELEGRAM_BOT_USERNAME ?? "";

export default function SellerDashboardPage() {
  const botHref = botUser
    ? `https://t.me/${botUser.replace(/^@/, "")}?start=seller`
    : null;

  return (
    <>
      <AppHeader title="Sotuvchi paneli" showBack backHref="/" />
      <main className="mx-auto max-w-lg space-y-6 px-4 pb-8 pt-4">
        <div className="rounded-3xl border border-amber-500/25 bg-gradient-to-br from-amber-500/15 to-violet-500/10 p-5">
          <div className="mb-2 inline-flex items-center gap-2 text-xs font-bold text-amber-800 dark:text-amber-200">
            <Sparkles className="h-4 w-4" />
            Do‘kon egasi rejimi
          </div>
          <p className="text-sm leading-relaxed text-foreground/90">
            Mahsulot e’lonlari va do‘konni <b>bot orqali</b> boshqaring — bu yerda
            tezkor havolalar va yo‘riqnoma.
          </p>
        </div>

        <div className="grid gap-3">
          <Button
            asChild
            variant="accent"
            className="h-auto min-h-14 justify-start gap-3 rounded-2xl py-4 text-left"
          >
            <Link href="/seller/shop">
              <Building2 className="h-5 w-5 shrink-0" />
              <span>
                <span className="block font-bold">🏪 Do‘konim</span>
                <span className="text-xs font-normal opacity-90">
                  Ma’lumot va tasdiq holati
                </span>
              </span>
            </Link>
          </Button>

          <Button
            asChild
            variant="outline"
            className="h-auto min-h-14 justify-start gap-3 rounded-2xl border-2 py-4 text-left"
          >
            <Link href="/seller/products">
              <Package className="h-5 w-5 shrink-0" />
              <span>
                <span className="block font-bold">📦 Mahsulotlarim</span>
                <span className="text-xs font-normal text-muted-foreground">
                  Ro‘yxat va faolsizlantirish (botda)
                </span>
              </span>
            </Link>
          </Button>

          {botHref ? (
            <Button
              asChild
              className="h-auto min-h-14 justify-start gap-3 rounded-2xl bg-stone-900 text-amber-50 hover:bg-stone-800"
            >
              <a href={botHref} target="_blank" rel="noreferrer">
                <Bot className="h-5 w-5 shrink-0" />
                <span>
                  <span className="block font-bold">➕ Mahsulot qo‘shish / e’lon</span>
                  <span className="text-xs font-normal opacity-90">
                    Botda yangi mahsulot yaratish
                  </span>
                </span>
              </a>
            </Button>
          ) : (
            <p className="rounded-2xl border border-dashed p-4 text-center text-sm text-muted-foreground">
              Bot havolasi uchun <code className="text-xs">NEXT_PUBLIC_TELEGRAM_BOT_USERNAME</code>{" "}
              ni .env ga qo‘shing.
            </p>
          )}
        </div>

        <p className="text-center text-xs text-muted-foreground">
          Mijozlar kabi katalogni ko‘rish uchun pastdagi <b>Bozor</b> yoki bosh sahifaga
          o‘ting.
        </p>
      </main>
    </>
  );
}
