"""Supabase helpers: users, products, shops, search logs, favorites, admin."""

import logging
from typing import Any

from supabase import Client, create_client

from app import config

logger = logging.getLogger(__name__)

_supabase: Client | None = None

SUBSCRIPTION_ORDER = {"vip": 0, "pro": 1, "free": 2}


def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        _supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    return _supabase


def _shop_from_product(p: dict[str, Any]) -> dict[str, Any]:
    raw = p.get("shops") or p.get("shop")
    return raw if isinstance(raw, dict) else {}


def sort_products_by_shop_tier(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    VIP do'konlar birinchi, keyin PRO, keyin FREE.
    Har bir darajada is_featured=true bo'lganlar oldinda.
    Bir xil guruhda asl qidiruv tartibi saqlanadi.
    """
    def key(item: tuple[int, dict[str, Any]]) -> tuple[int, int, int]:
        i, p = item
        shop = _shop_from_product(p)
        sub = str(shop.get("subscription_type") or "free").lower()
        tier = SUBSCRIPTION_ORDER.get(sub, 2)
        feat_rank = 0 if shop.get("is_featured") else 1
        return (tier, feat_rank, i)

    indexed = list(enumerate(products))
    indexed.sort(key=key)
    return [p for _, p in indexed]


def get_or_create_user_from_telegram(
    telegram_id: int,
    username: str | None,
    first_name: str | None,
    last_name: str | None,
) -> dict[str, Any] | None:
    """Upsert Telegram user; return user row."""
    sb = get_supabase()
    try:
        existing = (
            sb.table("users")
            .select("*")
            .eq("telegram_id", telegram_id)
            .limit(1)
            .execute()
        )
        if existing.data:
            row = existing.data[0]
            sb.table("users").update(
                {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                }
            ).eq("id", row["id"]).execute()
            row["username"] = username
            row["first_name"] = first_name
            row["last_name"] = last_name
            return row

        ins = (
            sb.table("users")
            .insert(
                {
                    "telegram_id": telegram_id,
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": "customer",
                }
            )
            .execute()
        )
        if ins.data:
            return ins.data[0]
    except Exception as e:
        logger.exception("get_or_create_user_from_telegram: %s", e)
    return None


def get_shop_by_id(shop_id: str) -> dict[str, Any] | None:
    sb = get_supabase()
    try:
        r = sb.table("shops").select("*").eq("id", shop_id).limit(1).execute()
        if r.data:
            return r.data[0]
    except Exception as e:
        logger.exception("get_shop_by_id: %s", e)
    return None


def _sort_shops_row(s: dict[str, Any]) -> tuple[int, int, str]:
    sub = str(s.get("subscription_type") or "free").lower()
    tier = SUBSCRIPTION_ORDER.get(sub, 2)
    feat = 0 if s.get("is_featured") else 1
    created = str(s.get("created_at") or "")
    return (tier, feat, created)


def list_shops(limit: int = 20) -> list[dict[str, Any]]:
    sb = get_supabase()
    try:
        r = (
            sb.table("shops")
            .select("*")
            .limit(min(limit * 2, 100))
            .execute()
        )
        rows = r.data or []
        rows.sort(key=_sort_shops_row)
        return rows[:limit]
    except Exception as e:
        logger.exception("list_shops: %s", e)
        return []


def list_latest_products(limit: int = 10) -> list[dict[str, Any]]:
    sb = get_supabase()
    try:
        r = (
            sb.table("products")
            .select("*, shops(*)")
            .eq("is_active", True)
            .order("created_at", desc=True)
            .limit(min(limit * 3, 50))
            .execute()
        )
        rows = sort_products_by_shop_tier(r.data or [])
        return rows[:limit]
    except Exception as e:
        logger.exception("list_latest_products: %s", e)
        return []


def _product_base_select(sb: Client):
    return sb.table("products").select("*, shops(*)").eq("is_active", True)


def _dedupe_preserve_order(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in rows:
        pid = str(row.get("id", ""))
        if pid and pid not in seen:
            seen.add(pid)
            out.append(row)
    return out


def search_products(
    search_terms: list[str],
    category: str | None = None,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """
    Qidiruv: kategoriya → kalit so'zlar → nom/tavsif.
    Natija premium tartibda (VIP → PRO → FREE, featured oldinda).
    """
    sb = get_supabase()
    lim = max(1, min(limit, 40))
    collected: list[dict[str, Any]] = []

    def run_ilike_column(column: str, pattern: str, fetch_limit: int) -> list[dict[str, Any]]:
        try:
            q = (
                _product_base_select(sb)
                .ilike(column, pattern)
                .limit(fetch_limit)
                .execute()
            )
            return q.data or []
        except Exception as e:
            logger.warning("search ilike %s: %s", column, e)
            return []

    try:
        if category:
            cat_pat = f"%{category.strip()}%"
            collected.extend(run_ilike_column("category", cat_pat, lim))

        for term in search_terms:
            if not term:
                continue
            pat = f"%{term.strip()}%"
            collected.extend(run_ilike_column("keywords", pat, lim))

        for term in search_terms:
            if not term:
                continue
            pat = f"%{term.strip()}%"
            collected.extend(run_ilike_column("name", pat, lim))
            collected.extend(run_ilike_column("description", pat, lim))

        merged = _dedupe_preserve_order(collected)
        ranked = sort_products_by_shop_tier(merged)
        return ranked[:lim]
    except Exception as e:
        logger.exception("search_products: %s", e)
        return []


def get_products_by_ids(ids: list[str]) -> list[dict[str, Any]]:
    """ID tartibini saqlab qaytaradi."""
    if not ids:
        return []
    sb = get_supabase()
    try:
        r = (
            sb.table("products")
            .select("*, shops(*)")
            .in_("id", ids)
            .eq("is_active", True)
            .execute()
        )
        data = r.data or []
        by_id = {str(x["id"]): x for x in data}
        return [by_id[i] for i in ids if i in by_id]
    except Exception as e:
        logger.exception("get_products_by_ids: %s", e)
        return []


def list_more_products_from_shop(
    shop_id: str,
    exclude_product_id: str | None,
    limit: int = 5,
) -> list[dict[str, Any]]:
    sb = get_supabase()
    try:
        q = (
            sb.table("products")
            .select("*, shops(*)")
            .eq("shop_id", shop_id)
            .eq("is_active", True)
            .limit(limit + 2)
            .execute()
        )
        rows = r.data or []
        if exclude_product_id:
            rows = [x for x in rows if str(x.get("id")) != exclude_product_id]
        rows = sort_products_by_shop_tier(rows)
        return rows[:limit]
    except Exception as e:
        logger.exception("list_more_products_from_shop: %s", e)
        return []


def filter_by_budget(products: list[dict[str, Any]], budget: int | None) -> list[dict[str, Any]]:
    if budget is None:
        return products
    out: list[dict[str, Any]] = []
    for p in products:
        pr = p.get("price")
        if pr is None:
            out.append(p)
            continue
        try:
            if float(pr) <= float(budget):
                out.append(p)
        except (TypeError, ValueError):
            out.append(p)
    return out


def log_search(
    user_id: str | None,
    user_query: str,
    interpreted_query: str,
) -> None:
    sb = get_supabase()
    try:
        payload: dict[str, Any] = {
            "user_query": user_query[:2000],
            "interpreted_query": interpreted_query[:2000],
        }
        if user_id:
            payload["user_id"] = user_id
        sb.table("search_logs").insert(payload).execute()
    except Exception as e:
        logger.warning("log_search failed: %s", e)


def _count_table(table: str) -> int:
    sb = get_supabase()
    try:
        r = sb.table(table).select("*", count="exact").limit(0).execute()
        return int(r.count or 0)
    except Exception as e:
        logger.warning("count %s: %s", table, e)
        return -1


def count_users() -> int:
    return _count_table("users")


def count_shops() -> int:
    return _count_table("shops")


def count_products() -> int:
    return _count_table("products")


def count_search_logs() -> int:
    return _count_table("search_logs")


def find_shop_by_name_substring(name_part: str) -> dict[str, Any] | None:
    part = (name_part or "").strip()
    if len(part) < 2:
        return None
    sb = get_supabase()
    try:
        r = (
            sb.table("shops")
            .select("*")
            .ilike("name", f"%{part}%")
            .limit(1)
            .execute()
        )
        if r.data:
            return r.data[0]
    except Exception as e:
        logger.exception("find_shop_by_name_substring: %s", e)
    return None


def insert_shop(
    owner_user_id: str,
    name: str,
    description: str | None,
    city: str | None,
    owner_telegram_username: str | None,
    subscription_type: str = "free",
    is_featured: bool = False,
) -> dict[str, Any] | None:
    sb = get_supabase()
    try:
        row = {
            "owner_user_id": owner_user_id,
            "name": name,
            "description": description or "",
            "city": city or "",
            "owner_telegram_username": owner_telegram_username,
            "subscription_type": subscription_type,
            "is_featured": is_featured,
        }
        r = sb.table("shops").insert(row).execute()
        if r.data:
            return r.data[0]
    except Exception as e:
        logger.exception("insert_shop: %s", e)
    return None


def insert_product(
    shop_id: str,
    name: str,
    description: str | None,
    price: float | None,
    category: str | None,
    keywords: str | None,
    stock: int = 0,
) -> dict[str, Any] | None:
    sb = get_supabase()
    try:
        row: dict[str, Any] = {
            "shop_id": shop_id,
            "name": name,
            "description": description or "",
            "price": price,
            "category": category or "",
            "keywords": keywords or "",
            "stock": stock,
            "is_active": True,
        }
        r = sb.table("products").insert(row).execute()
        if r.data:
            return r.data[0]
    except Exception as e:
        logger.exception("insert_product: %s", e)
    return None


def set_shop_featured(shop_id: str, featured: bool) -> bool:
    sb = get_supabase()
    try:
        sb.table("shops").update({"is_featured": featured}).eq("id", shop_id).execute()
        return True
    except Exception as e:
        logger.exception("set_shop_featured: %s", e)
        return False


def set_shop_subscription(shop_id: str, subscription_type: str) -> bool:
    sub = subscription_type.lower().strip()
    if sub not in SUBSCRIPTION_ORDER:
        return False
    sb = get_supabase()
    try:
        sb.table("shops").update({"subscription_type": sub}).eq("id", shop_id).execute()
        return True
    except Exception as e:
        logger.exception("set_shop_subscription: %s", e)
        return False


def get_or_create_user_by_telegram_id_only(
    telegram_id: int,
    username: str | None = None,
) -> dict[str, Any] | None:
    """Admin: sotuvchi uchun minimal foydalanuvchi."""
    return get_or_create_user_from_telegram(
        telegram_id=telegram_id,
        username=username,
        first_name=None,
        last_name=None,
    )


def favorited_map_for_user(
    user_uuid: str | None, product_ids: list[str]
) -> dict[str, bool]:
    if not user_uuid:
        return {}
    return {pid: is_product_favorited(user_uuid, pid) for pid in product_ids}


def is_product_favorited(user_uuid: str, product_id: str) -> bool:
    sb = get_supabase()
    try:
        r = (
            sb.table("user_favorites")
            .select("product_id")
            .eq("user_id", user_uuid)
            .eq("product_id", product_id)
            .limit(1)
            .execute()
        )
        return bool(r.data)
    except Exception as e:
        logger.warning("is_product_favorited: %s", e)
        return False


def toggle_favorite(user_uuid: str, product_id: str) -> tuple[bool, bool]:
    """
    Saqlashni almashtiradi.
    Qaytadi: (muvaffaqiyat, hozir_saqlanganmi).
    """
    sb = get_supabase()
    try:
        if is_product_favorited(user_uuid, product_id):
            sb.table("user_favorites").delete().eq("user_id", user_uuid).eq(
                "product_id", product_id
            ).execute()
            return True, False
        sb.table("user_favorites").insert(
            {"user_id": user_uuid, "product_id": product_id}
        ).execute()
        return True, True
    except Exception as e:
        logger.warning("toggle_favorite: %s", e)
        return False, False
