"use client";

import { useAppRole } from "@/components/RoleProvider";

/**
 * Telegram ichida rol doimiy “mijoz” bo‘lib qolsa — odatda server env yetishmaydi.
 */
export function RoleConfigBanner() {
  const { roleHint } = useAppRole();
  if (!roleHint) return null;

  return (
    <div className="sticky top-0 z-[90] border-b border-sky-900/30 bg-sky-950 px-3 py-2.5 text-center text-xs text-sky-50">
      <strong className="block font-semibold">ℹ️ Rol aniqlanmadi (mijoz ko‘rinishi)</strong>
      <span className="mt-1 block opacity-95">{roleHint}</span>
    </div>
  );
}
