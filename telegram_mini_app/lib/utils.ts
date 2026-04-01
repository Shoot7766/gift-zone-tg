import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPriceUZS(n: number | null | undefined): string {
  if (n == null || Number.isNaN(Number(n))) return "Kelishiladi";
  return `${Math.round(Number(n)).toLocaleString("uz-UZ")} so'm`;
}
