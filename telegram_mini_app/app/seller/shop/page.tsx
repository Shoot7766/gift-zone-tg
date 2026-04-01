"use client";

import Link from "next/link";
import { AppHeader } from "@/components/AppHeader";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Building2 } from "lucide-react";

const botUser = process.env.NEXT_PUBLIC_TELEGRAM_BOT_USERNAME ?? "";

export default function SellerShopPage() {
  const botHref = botUser
    ? `https://t.me/${botUser.replace(/^@/, "")}?start=seller`
    : null;

  return (
    <>
      <AppHeader title="Do‘konim" showBack backHref="/seller" />
      <main className="mx-auto max-w-lg space-y-5 px-4 pb-8 pt-4">
        <div className="flex items-start gap-3 rounded-2xl border bg-card p-4 shadow-sm">
          <Building2 className="mt-0.5 h-8 w-8 text-amber-600" />
          <div className="space-y-2 text-sm leading-relaxed">
            <p>
              Do‘kon <b>yaratish va tahrirlash</b> Telegram botda amalga oshiriladi:
              botda <b>🏪 Do‘konim</b> tugmasini bosing.
            </p>
            <p className="text-muted-foreground">
              Do‘kon <b>admin tasdig‘idan</b> keyin barcha mijozlarga (mini ilova va qidiruvda)
              ko‘rinadi. Tasdiqlanmagan do‘konlar ommaviy ro‘yxatlarda chiqmaydi.
            </p>
          </div>
        </div>

        {botHref ? (
          <Button asChild className="w-full rounded-2xl font-bold" size="lg">
            <a href={botHref} target="_blank" rel="noreferrer">
              Botda do‘konni boshqarish
            </a>
          </Button>
        ) : null}

        <Button variant="ghost" asChild className="w-full rounded-2xl">
          <Link href="/seller">
            <ArrowLeft className="h-4 w-4" />
            Panelga qaytish
          </Link>
        </Button>
      </main>
    </>
  );
}
