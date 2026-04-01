"use client";

import Link from "next/link";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import { Package } from "lucide-react";

const botUser = process.env.NEXT_PUBLIC_TELEGRAM_BOT_USERNAME ?? "";

export default function SellerProductsPage() {
  const botHref = botUser
    ? `https://t.me/${botUser.replace(/^@/, "")}?start=seller`
    : null;

  return (
    <>
      <AppHeader title="Mahsulotlarim" showBack backHref="/seller" />
      <main className="mx-auto max-w-lg space-y-5 px-4 pb-8 pt-4">
        <div className="rounded-2xl border bg-card p-4 text-sm leading-relaxed shadow-sm">
          <div className="mb-2 flex items-center gap-2 font-bold">
            <Package className="h-5 w-5 text-amber-600" />
            E’lonlar (mahsulotlar)
          </div>
          <p className="text-muted-foreground">
            Yangi mahsulot qo‘shish va ro‘yxatni ko‘rish botda:{" "}
            <b>📦 Mahsulotlarim</b> yoki <b>➕ Mahsulot qo‘shish</b>.
          </p>
          <p className="mt-3 text-muted-foreground">
            Mahsulotni yashirish: botda{" "}
            <code className="rounded bg-muted px-1 text-xs">/mahsulot_off</code>{" "}
            va mahsulot UUID sini yuboring (ro‘yxatda ko‘rsatiladi).
          </p>
        </div>

        {botHref ? (
          <Button asChild className="w-full rounded-2xl font-bold" size="lg">
            <a href={botHref} target="_blank" rel="noreferrer">
              Botda mahsulotlarni boshqarish
            </a>
          </Button>
        ) : (
          <p className="text-center text-sm text-muted-foreground">
            Bot username sozlanmagan.
          </p>
        )}

        <Button variant="outline" asChild className="w-full rounded-2xl">
          <Link href="/seller">Orqaga</Link>
        </Button>
      </main>
    </>
  );
}
