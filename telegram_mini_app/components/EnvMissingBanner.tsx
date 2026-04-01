/** Server: build vaqtida env mavjudligini tekshiradi */
export function EnvMissingBanner() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY?.trim();
  if (url && key) return null;

  return (
    <div className="sticky top-0 z-[100] border-b border-amber-800/40 bg-amber-950 px-4 py-3 text-center text-sm text-amber-50">
      <strong className="block">⚠️ Supabase sozlamalari yo‘q</strong>
      <span className="mt-1 block opacity-90">
        Vercel → Project → Settings → Environment Variables ga{" "}
        <code className="rounded bg-black/30 px-1">NEXT_PUBLIC_SUPABASE_URL</code> va{" "}
        <code className="rounded bg-black/30 px-1">NEXT_PUBLIC_SUPABASE_ANON_KEY</code>{" "}
        qo‘shing, keyin <strong>Redeploy</strong> qiling.
      </span>
    </div>
  );
}
