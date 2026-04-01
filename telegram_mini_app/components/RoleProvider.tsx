"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

export type AppUserRole = "customer" | "seller" | "admin";

type RoleState = {
  role: AppUserRole;
  loading: boolean;
  telegramId: number | null;
  refresh: () => void;
};

const RoleContext = createContext<RoleState | null>(null);

export function RoleProvider({ children }: { children: React.ReactNode }) {
  const [role, setRole] = useState<AppUserRole>("customer");
  const [loading, setLoading] = useState(true);
  const [telegramId, setTelegramId] = useState<number | null>(null);
  const [tick, setTick] = useState(0);

  const refresh = useCallback(() => setTick((t) => t + 1), []);

  useEffect(() => {
    let cancelled = false;
    const run = async () => {
      const initData =
        typeof window !== "undefined"
          ? window.Telegram?.WebApp?.initData ?? ""
          : "";
      if (!initData) {
        if (!cancelled) {
          setRole("customer");
          setLoading(false);
          setTelegramId(
            window.Telegram?.WebApp?.initDataUnsafe?.user?.id ?? null
          );
        }
        return;
      }
      try {
        const res = await fetch("/api/me", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ initData }),
        });
        const j = (await res.json()) as {
          role?: string;
          telegramId?: number;
        };
        if (cancelled) return;
        const r = j.role;
        setTelegramId(j.telegramId ?? null);
        if (r === "seller" || r === "admin") setRole(r);
        else setRole("customer");
      } catch {
        if (!cancelled) setRole("customer");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    setLoading(true);
    run();
    return () => {
      cancelled = true;
    };
  }, [tick]);

  const value = useMemo(
    () => ({ role, loading, telegramId, refresh }),
    [role, loading, telegramId, refresh]
  );

  return (
    <RoleContext.Provider value={value}>{children}</RoleContext.Provider>
  );
}

export function useAppRole() {
  const ctx = useContext(RoleContext);
  if (!ctx) {
    return {
      role: "customer" as AppUserRole,
      loading: false,
      telegramId: null,
      refresh: () => {},
    };
  }
  return ctx;
}
