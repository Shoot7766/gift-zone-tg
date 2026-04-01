import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

type Props = { count?: number; className?: string };

export function ProductGridSkeleton({ count = 4, className }: Props) {
  return (
    <div className={cn("grid grid-cols-2 gap-3", className)}>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="overflow-hidden rounded-2xl border border-border/40 bg-card/50 shadow-sm"
        >
          <Skeleton className="aspect-[3/4] w-full rounded-none" />
          <div className="space-y-2 p-3">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-2/3" />
            <Skeleton className="h-8 w-full rounded-xl" />
            <Skeleton className="h-8 w-full rounded-xl" />
          </div>
        </div>
      ))}
    </div>
  );
}
