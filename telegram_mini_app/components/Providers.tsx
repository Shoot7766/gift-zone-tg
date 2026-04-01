"use client";

import { useEffect } from "react";
import { RoleProvider } from "@/components/RoleProvider";
import { initTelegramWebApp } from "@/lib/telegram";

export function Providers({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    initTelegramWebApp();
  }, []);
  return <RoleProvider>{children}</RoleProvider>;
}
