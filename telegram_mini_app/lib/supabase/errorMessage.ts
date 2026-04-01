/** Supabase/PostgREST xatosi ba'zan `Error` emas — matnni chiqarish uchun */
export function supabaseFetchErrorMessage(
  e: unknown,
  fallback = "Ma'lumot yuklanmadi. .env va Supabase RLS ni tekshiring."
): string {
  if (e instanceof Error) return e.message;
  if (
    e &&
    typeof e === "object" &&
    "message" in e &&
    typeof (e as { message: unknown }).message === "string"
  ) {
    return (e as { message: string }).message;
  }
  return fallback;
}
