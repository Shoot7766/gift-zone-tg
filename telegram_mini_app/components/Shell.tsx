import { BottomNav } from "@/components/BottomNav";

export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="tg-viewport min-h-dvh pb-24">
      {children}
      <BottomNav />
    </div>
  );
}
