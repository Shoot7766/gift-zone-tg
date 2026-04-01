"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, LayoutGrid, Store, Heart } from "lucide-react";
import { cn } from "@/lib/utils";

const items = [
  { href: "/", label: "Bosh sahifa", icon: Home },
  { href: "/products", label: "Mahsulotlar", icon: LayoutGrid },
  { href: "/shops", label: "Do'konlar", icon: Store },
  { href: "/favorites", label: "Saqlanganlar", icon: Heart },
] as const;

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-border/50 bg-background/95 pb-[env(safe-area-inset-bottom)] shadow-[0_-8px_32px_-12px_rgba(0,0,0,0.12)] backdrop-blur-xl dark:shadow-[0_-8px_32px_-12px_rgba(0,0,0,0.4)]">
      <div className="mx-auto flex max-w-lg items-stretch justify-between gap-1 px-2 pt-1.5">
        {items.map(({ href, label, icon: Icon }) => {
          const active =
            href === "/"
              ? pathname === "/"
              : pathname === href || pathname.startsWith(href + "/");
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex min-w-0 flex-1 flex-col items-center gap-0.5 rounded-2xl py-2.5 text-[10px] font-bold transition-all duration-200",
                active
                  ? "bg-gradient-to-b from-amber-500/20 to-amber-600/10 text-amber-800 shadow-inner dark:from-amber-500/25 dark:to-amber-600/5 dark:text-amber-200"
                  : "text-muted-foreground hover:bg-muted/60 hover:text-foreground"
              )}
            >
              <span
                className={cn(
                  "flex h-9 w-9 items-center justify-center rounded-xl transition-transform",
                  active && "scale-105 bg-amber-500/15 dark:bg-amber-400/10"
                )}
              >
                <Icon
                  className={cn("h-5 w-5", active && "text-amber-700 dark:text-amber-300")}
                  strokeWidth={active ? 2.5 : 2}
                />
              </span>
              <span className="truncate px-0.5">{label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
