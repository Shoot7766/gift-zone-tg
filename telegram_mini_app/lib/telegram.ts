"use client";

import { useEffect, useState } from "react";

export type TelegramUser = {
  id: number;
  first_name?: string;
  last_name?: string;
  username?: string;
};

declare global {
  interface Window {
    Telegram?: {
      WebApp: {
        ready: () => void;
        expand: () => void;
        close: () => void;
        BackButton: { show: () => void; hide: () => void; onClick: (cb: () => void) => void };
        MainButton: { text: string; show: () => void; hide: () => void };
        themeParams: Record<string, string | undefined>;
        initDataUnsafe?: { user?: TelegramUser };
        version: string;
        platform: string;
      };
    };
  }
}

export function initTelegramWebApp() {
  if (typeof window === "undefined") return;
  const w = window.Telegram?.WebApp;
  if (w) {
    w.ready();
    w.expand();
  }
}

export function useTelegramUser() {
  const [user, setUser] = useState<TelegramUser | null>(null);
  const [inTelegram, setInTelegram] = useState(false);

  useEffect(() => {
    initTelegramWebApp();
    const u = window.Telegram?.WebApp?.initDataUnsafe?.user;
    setInTelegram(!!window.Telegram?.WebApp);
    if (u) setUser(u);
  }, []);

  return { user, inTelegram };
}

export function openTelegramUser(username: string) {
  const u = username.replace(/^@/, "");
  window.open(`https://t.me/${u}`, "_blank");
}

export function closeMiniApp() {
  window.Telegram?.WebApp?.close();
}
