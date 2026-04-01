"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import type { RoleSource } from "@/lib/roleSource";

export type AppUserRole = "customer" | "seller" | "admin";

type RoleState = {
  role: AppUserRole;
  loading: boolean;
  telegramId: number | null;
  roleSource: RoleSource | null;
  /** Telegram ichida env/xato bo‘lsa — foydalanuvchiga ko‘rsatiladigan matn */
  roleHint: string | null;
  refresh: () => void;
};

const RoleContext = createContext<RoleState | null>(null);

function hintForSource(source: RoleSource | undefined): string | null {
  switch (source) {
    case "fallback_no_service_key":
      return (
        "Vercel (yoki server) da quyidagilarni qo‘shing va qayta deploy qiling: " +
        "TELEGRAM_BOT_TOKEN, SUPABASE_SERVICE_ROLE_KEY, " +
        "NEXT_PUBLIC_SUPABASE_URL (yoki SUPABASE_URL). " +
        "Shularsiz barcha foydalanuvchilar «mijoz» navigatsiyasini ko‘radi."
      );
    case "missing_bot_token":
      return (
        "TELEGRAM_BOT_TOKEN serverda yo‘q — initData tekshirilmaydi. " +
        "Vercel → Environment Variables ga bot tokenini qo‘shing (Production)."
      );
    case "fallback_no_user_row":
      return (
        "Siz hali bazada yo‘qsiz yoki telegram_id mos kelmayapti. " +
        "Botda /start yuboring va rolni tanlang (Mijoz yoki Do‘kon egasi)."
      );
    case "invalid_init_data":
      return "Telegram ma’lumoti eskirgan yoki buzilgan. Mini ilovani yoping va qayta oching.";
    case "server_error":
      return "Serverda xato. Bir ozdan keyin sahifani yangilang.";
    default:
      return null;
  }
}

export function RoleProvider({ children }: { children: React.ReactNode }) {
  const [role, setRole] = useState<AppUserRole>("customer");
  const [loading, setLoading] = useState(true);
  const [telegramId, setTelegramId] = useState<number | null>(null);
  const [roleSource, setRoleSource] = useState<RoleSource | null>(null);
  const [roleHint, setRoleHint] = useState<string | null>(null);
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
          setRoleSource("no_telegram_auth");
          setRoleHint(null);
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
          roleSource?: RoleSource;
        };
        if (cancelled) return;
        const src = j.roleSource;
        setRoleSource(src ?? null);
        setTelegramId(j.telegramId ?? null);

        const r = j.role;
        if (r === "seller" || r === "admin") {
          setRole(r);
          setRoleHint(null);
        } else {
          setRole("customer");
          setRoleHint(
            res.ok && src && src !== "database" ? hintForSource(src) : null
          );
          if (!res.ok && src === "invalid_init_data") {
            setRoleHint(hintForSource("invalid_init_data"));
          }
        }
      } catch {
        if (!cancelled) {
          setRole("customer");
          setRoleSource("server_error");
          setRoleHint(hintForSource("server_error"));
        }
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
    () => ({
      role,
      loading,
      telegramId,
      roleSource,
      roleHint,
      refresh,
    }),
    [role, loading, telegramId, roleSource, roleHint, refresh]
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
      roleSource: null,
      roleHint: null,
      refresh: () => {},
    };
  }
  return ctx;
}
