import { BottomNav } from "@/components/BottomNav";
import { RoleConfigBanner } from "@/components/RoleConfigBanner";

export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="tg-viewport min-h-dvh pb-24">
      <RoleConfigBanner />
      {children}
      <BottomNav />
    </div>
  );
}
