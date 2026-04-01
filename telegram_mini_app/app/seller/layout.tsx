"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAppRole } from "@/components/RoleProvider";
import { Skeleton } from "@/components/ui/skeleton";

export default function SellerSectionLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { role, loading } = useAppRole();
  const router = useRouter();

  useEffect(() => {
    if (!loading && role !== "seller" && role !== "admin") {
      router.replace("/");
    }
  }, [loading, role, router]);

  if (loading) {
    return (
      <div className="mx-auto max-w-lg space-y-4 px-4 py-12">
        <Skeleton className="mx-auto h-8 w-48 rounded-xl" />
        <Skeleton className="h-24 w-full rounded-2xl" />
      </div>
    );
  }

  if (role !== "seller" && role !== "admin") {
    return null;
  }

  return <>{children}</>;
}
