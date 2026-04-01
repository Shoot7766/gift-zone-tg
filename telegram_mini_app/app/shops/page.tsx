"use client";

import { useEffect, useState } from "react";
import { AppHeader } from "@/components/AppHeader";
import { ShopCard } from "@/components/ShopCard";
import { EmptyState } from "@/components/EmptyState";
import { Skeleton } from "@/components/ui/skeleton";
import { fetchShops } from "@/lib/supabase/queries";
import type { Shop } from "@/types";
import { Store } from "lucide-react";

export default function ShopsPage() {
  const [shops, setShops] = useState<Shop[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchShops()
      .then(setShops)
      .catch(() => setShops([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <>
      <AppHeader title="Do'konlar" showBack backHref="/" />
      <main className="mx-auto max-w-lg space-y-4 px-4 pb-8 pt-4">
        <p className="text-sm text-muted-foreground">
          VIP va tavsiya etilgan do&apos;konlar yuqorida ko&apos;rsatiladi.
        </p>
        {loading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-36 rounded-2xl" />
            ))}
          </div>
        ) : shops.length === 0 ? (
          <EmptyState
            icon={Store}
            title="Do'konlar yo'q"
            description="Tez orada yangi do'konlar qo'shiladi."
          />
        ) : (
          <div className="space-y-3">
            {shops.map((s) => (
              <ShopCard key={s.id} shop={s} />
            ))}
          </div>
        )}
      </main>
    </>
  );
}
