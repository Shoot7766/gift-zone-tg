const KEY = "gift-zone-mini-favorites";

export function getFavoriteIds(): string[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return [];
    const arr = JSON.parse(raw) as unknown;
    return Array.isArray(arr) ? arr.filter((x) => typeof x === "string") : [];
  } catch {
    return [];
  }
}

export function toggleFavoriteId(id: string): boolean {
  const cur = getFavoriteIds();
  const has = cur.includes(id);
  const next = has ? cur.filter((x) => x !== id) : [...cur, id];
  localStorage.setItem(KEY, JSON.stringify(next));
  return !has;
}

export function isFavoriteId(id: string): boolean {
  return getFavoriteIds().includes(id);
}

export function removeFavoriteId(id: string): void {
  const next = getFavoriteIds().filter((x) => x !== id);
  localStorage.setItem(KEY, JSON.stringify(next));
}
