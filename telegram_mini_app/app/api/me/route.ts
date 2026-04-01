import { createClient } from "@supabase/supabase-js";
import crypto from "crypto";
import { NextResponse } from "next/server";

import type { RoleSource } from "@/lib/roleSource";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

function parseAdminTelegramIds(): Set<number> {
  const raw = process.env.ADMIN_TELEGRAM_IDS?.replace(/\s/g, "") ?? "";
  const out = new Set<number>();
  for (const part of raw.split(",")) {
    if (/^\d+$/.test(part)) out.add(Number(part));
  }
  return out;
}

function verifyTelegramInitData(
  initData: string,
  botToken: string
): { telegramId: number } | null {
  const params = new URLSearchParams(initData);
  const hash = params.get("hash");
  if (!hash) return null;
  params.delete("hash");
  const entries = Array.from(params.entries()).sort(([a], [b]) =>
    a.localeCompare(b)
  );
  const dataCheckString = entries.map(([k, v]) => `${k}=${v}`).join("\n");
  const secretKey = crypto.createHmac("sha256", "WebAppData").update(botToken).digest();
  const h = crypto.createHmac("sha256", secretKey).update(dataCheckString).digest("hex");
  if (h !== hash) return null;
  const userJson = params.get("user");
  if (!userJson) return null;
  try {
    const user = JSON.parse(userJson) as { id?: number };
    if (typeof user.id !== "number") return null;
    return { telegramId: user.id };
  } catch {
    return null;
  }
}

/**
 * Telegram WebApp initData ni tekshiradi va Supabase users jadvalidan rol qaytaradi.
 * SUPABASE_SERVICE_ROLE_KEY bo‘lmasa — xavfsiz default: customer + roleSource.
 */
export async function POST(request: Request) {
  try {
    const body = (await request.json()) as { initData?: string };
    const initData = body.initData ?? "";
    const botToken = process.env.TELEGRAM_BOT_TOKEN?.trim() ?? "";

    if (!initData) {
      return NextResponse.json({
        role: "customer" as const,
        roleSource: "no_telegram_auth" as const,
      });
    }

    if (!botToken) {
      return NextResponse.json({
        role: "customer" as const,
        roleSource: "missing_bot_token" as const,
      });
    }

    const verified = verifyTelegramInitData(initData, botToken);
    if (!verified) {
      return NextResponse.json(
        {
          error: "invalid_init_data",
          roleSource: "invalid_init_data" as const,
        },
        { status: 401 }
      );
    }

    if (parseAdminTelegramIds().has(verified.telegramId)) {
      return NextResponse.json({
        role: "admin" as const,
        telegramId: verified.telegramId,
        roleSource: "admin_env" as const,
      });
    }

    const url =
      process.env.SUPABASE_URL?.trim() || process.env.NEXT_PUBLIC_SUPABASE_URL?.trim() || "";
    const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY?.trim() ?? "";
    if (!url || !serviceKey) {
      return NextResponse.json({
        role: "customer" as const,
        telegramId: verified.telegramId,
        roleSource: "fallback_no_service_key" as const,
      });
    }

    const sb = createClient(url, serviceKey);
    const { data, error } = await sb
      .from("users")
      .select("id, role")
      .eq("telegram_id", verified.telegramId)
      .maybeSingle();

    if (error || !data) {
      return NextResponse.json({
        role: "customer" as const,
        telegramId: verified.telegramId,
        roleSource: "fallback_no_user_row" as const,
      });
    }

    const r = data.role as string;
    const role =
      r === "seller" || r === "admin" || r === "customer" ? r : "customer";

    return NextResponse.json({
      role,
      userId: data.id as string,
      telegramId: verified.telegramId,
      roleSource: "database" as const,
    });
  } catch {
    return NextResponse.json({
      role: "customer" as const,
      roleSource: "server_error" as const,
    });
  }
}
