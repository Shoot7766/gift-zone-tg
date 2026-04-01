import { cn } from "@/lib/utils";
import { Users, Zap } from "lucide-react";

type Props = { className?: string; dense?: boolean };

/** Sotuvchilarga ishonch (keyin real statistikaga almashtirish mumkin) */
export function TrustStrip({ className, dense }: Props) {
  return (
    <div
      className={cn(
        "flex flex-wrap items-center gap-x-4 gap-y-2 rounded-2xl border border-border/50 bg-muted/40 px-4 py-3 text-xs text-muted-foreground",
        dense && "py-2",
        className
      )}
    >
      <span className="inline-flex items-center gap-1.5 font-medium text-foreground/85">
        <Users className="h-3.5 w-3.5 text-amber-600 dark:text-amber-400" />
        100+ mijoz tanladi
      </span>
      <span className="hidden h-3 w-px bg-border sm:inline" aria-hidden />
      <span className="inline-flex items-center gap-1.5 font-medium text-foreground/85">
        <Zap className="h-3.5 w-3.5 text-amber-600 dark:text-amber-400" />
        Tez javob beradi
      </span>
    </div>
  );
}
