"use client";

import Image from "next/image";
import { cn } from "@/lib/utils";
import { Gift } from "lucide-react";

type Props = {
  src: string | null | undefined;
  alt: string;
  className?: string;
  priority?: boolean;
};

export function ProductImage({ src, alt, className, priority }: Props) {
  if (src) {
    return (
      <div className={cn("relative overflow-hidden bg-muted", className)}>
        <Image
          src={src}
          alt={alt}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, 400px"
          priority={priority}
          unoptimized
        />
      </div>
    );
  }
  return (
    <div
      className={cn(
        "flex items-center justify-center bg-gradient-to-br from-amber-100 via-stone-100 to-stone-200 dark:from-amber-950/40 dark:via-stone-900 dark:to-stone-950",
        className
      )}
    >
      <Gift className="h-12 w-12 text-amber-700/50 dark:text-amber-400/40" strokeWidth={1.25} />
    </div>
  );
}
