"use client";

import { MessageCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { openTelegramUser } from "@/lib/telegram";

type Props = {
  username: string | null | undefined;
  className?: string;
  size?: "default" | "lg";
};

export function SellerContactButton({ username, className, size = "default" }: Props) {
  if (!username?.trim()) {
    return (
      <Button variant="outline" disabled className={className} size={size === "lg" ? "lg" : "default"}>
        Username yo&apos;q
      </Button>
    );
  }
  const u = username.replace(/^@/, "");
  return (
    <Button
      type="button"
      variant="accent"
      size={size === "lg" ? "lg" : "default"}
      className={className}
      onClick={() => openTelegramUser(u)}
    >
      <MessageCircle className="h-4 w-4" />
      Sotuvchiga yozish
    </Button>
  );
}
