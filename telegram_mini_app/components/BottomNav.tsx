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
    <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-border/60 bg-background/90 pb-[env(safe-area-inset-bottom)] backdrop-blur-xl">
      <div className="mx-auto flex max-w-lg items-stretch justify-around px-2 pt-2">
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
                "flex min-w-0 flex-1 flex-col items-center gap-1 rounded-xl py-2 text-[10px] font-semibold transition-colors",
                active
                  ? "text-amber-700 dark:text-amber-400"
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              <Icon
                className={cn(
                  "h-5 w-5",
                  active && "scale-110 drop-shadow-sm"
                )}
                strokeWidth={active ? 2.25 : 2}
              />
              <span className="truncate px-0.5">{label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
