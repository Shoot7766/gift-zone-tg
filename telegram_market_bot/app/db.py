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


def user_registration_complete(row: dict[str, Any] | None) -> bool:
    """Telefon va rol to‘ldirilgan bo‘lsa — ro‘yxatdan o‘tgan."""
    if not row:
        return False
    phone = (row.get("phone_number") or "").strip()
    role = row.get("role")
    return bool(phone) and role in ("customer", "seller", "admin")


def get_user_by_telegram_id(telegram_id: int) -> dict[str, Any] | None:
    sb = get_supabase()
    try:
        r = (
            sb.table("users")
            .select("*")
            .eq("telegram_id", telegram_id)
            .limit(1)
            .execute()
        )
        if r.data:
            return r.data[0]
    except Exception as e:
        logger.exception("get_user_by_telegram_id: %s", e)
    return None


def create_user_with_role(
    telegram_id: int,
    username: str | None,
    first_name: str | None,
    last_name: str | None,
    role: str,
) -> dict[str, Any] | None:
    if role not in ("customer", "seller", "admin"):
        return None
    sb = get_supabase()
    try:
        ins = (
            sb.table("users")
            .insert(
                {
                    "telegram_id": telegram_id,
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": role,
                    "is_registered": False,
                }
            )
            .execute()
        )
        if ins.data:
            return ins.data[0]
    except Exception as e:
        logger.exception("create_user_with_role: %s", e)
    return None


def insert_full_registration(
    telegram_id: int,
    username: str | None,
    first_name: str | None,
    last_name: str | None,
    phone_number: str,
    role: str,
) -> dict[str, Any] | None:
    """Yangi foydalanuvchi: telefon + rol (faqat mijoz / sotuvchi)."""
    if role not in ("customer", "seller"):
        return None
    phone = (phone_number or "").strip()
    if not phone:
        return None
    sb = get_supabase()
    try:
        ins = (
            sb.table("users")
            .insert(
                {
                    "telegram_id": telegram_id,
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone_number": phone,
                    "role": role,
                    "is_registered": True,
                }
            )
            .execute()
        )
        if ins.data:
            return ins.data[0]
    except Exception as e:
        logger.exception("insert_full_registration: %s", e)
    return None


def update_user_phone(telegram_id: int, phone_number: str) -> dict[str, Any] | None:
    row = get_user_by_telegram_id(telegram_id)
    if not row:
        return None
    phone = (phone_number or "").strip()
    if not phone:
        return None
    merged = {**row, "phone_number": phone}
    reg = user_registration_complete(merged)
    sb = get_supabase()
    try:
        sb.table("users").update(
            {"phone_number": phone, "is_registered": reg}
        ).eq("id", row["id"]).execute()
        return get_user_by_telegram_id(telegram_id)
    except Exception as e:
        logger.exception("update_user_phone: %s", e)
    return None


def update_user_role_for_registration(telegram_id: int, role: str) -> dict[str, Any] | None:
    if role not in ("customer", "seller"):
        return None
    row = get_user_by_telegram_id(telegram_id)
    if not row:
        return None
    merged = {**row, "role": role}
    reg = user_registration_complete(merged)
    sb = get_supabase()
    try:
        sb.table("users").update({"role": role, "is_registered": reg}).eq(
            "id", row["id"]
        ).execute()
        return get_user_by_telegram_id(telegram_id)
    except Exception as e:
        logger.exception("update_user_role_for_registration: %s", e)
    return None


def update_user_profile(
    telegram_id: int,
    username: str | None,
    first_name: str | None,
    last_name: str | None,
) -> dict[str, Any] | None:
    row = get_user_by_telegram_id(telegram_id)
    if not row:
        return None
    sb = get_supabase()
    try:
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
    except Exception as e:
        logger.exception("update_user_profile: %s", e)
    return None


def get_or_create_user_from_telegram(
    telegram_id: int,
    username: str | None,
    first_name: str | None,
    last_name: str | None,
) -> dict[str, Any] | None:
    """
    Faqat allaqachon ro'yxatdan o'tgan foydalanuvchi (/start da rol tanlagan).
    Yangi foydalanuvchi uchun None — avval rol tanlash kerak.
    """
    return update_user_profile(telegram_id, username, first_name, last_name)


def ensure_seller_user_for_admin(
    telegram_id: int,
    username: str | None,
) -> dict[str, Any] | None:
    """Admin do'kon qo'shganda: foydalanuvchi bo'lmasa sotuvchi sifatida yaratiladi."""
    row = get_user_by_telegram_id(telegram_id)
    if row:
        return row
    return create_user_with_role(telegram_id, username, None, None, "seller")


def _shop_approved(shop: dict[str, Any]) -> bool:
    return shop.get("is_approved") is True


def filter_public_products(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [p for p in products if _shop_approved(_shop_from_product(p))]


def get_product_by_id(product_id: str) -> dict[str, Any] | None:
    sb = get_supabase()
    try:
        r = sb.table("products").select("*").eq("id", product_id).limit(1).execute()
        if r.data:
            return r.data[0]
    except Exception as e:
        logger.exception("get_product_by_id: %s", e)
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


def list_shops(limit: int = 20, *, approved_only: bool = True) -> list[dict[str, Any]]:
    sb = get_supabase()
    try:
        q = sb.table("shops").select("*")
        if approved_only:
            q = q.eq("is_approved", True)
        r = q.limit(min(limit * 2, 100)).execute()
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
        rows = filter_public_products(sort_products_by_shop_tier(r.data or []))
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

        merged = filter_public_products(
            sort_products_by_shop_tier(_dedupe_preserve_order(collected))
        )
        return merged[:lim]
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
        data = filter_public_products(r.data or [])
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
        rows = filter_public_products(r.data or [])
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
    *,
    is_approved: bool = False,
    logo_url: str | None = None,
    banner_url: str | None = None,
) -> dict[str, Any] | None:
    sb = get_supabase()
    try:
        row: dict[str, Any] = {
            "owner_user_id": owner_user_id,
            "name": name,
            "description": description or "",
            "city": city or "",
            "owner_telegram_username": owner_telegram_username,
            "subscription_type": subscription_type,
            "is_featured": is_featured,
            "is_approved": is_approved,
        }
        if logo_url is not None:
            row["logo_url"] = logo_url
        if banner_url is not None:
            row["banner_url"] = banner_url
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
    image_url: str | None = None,
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
        if image_url:
            row["image_url"] = image_url.strip()
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


def set_shop_approved(shop_id: str, approved: bool) -> bool:
    sb = get_supabase()
    try:
        sb.table("shops").update({"is_approved": approved}).eq("id", shop_id).execute()
        return True
    except Exception as e:
        logger.exception("set_shop_approved: %s", e)
        return False


def list_pending_shops(limit: int = 25) -> list[dict[str, Any]]:
    sb = get_supabase()
    try:
        r = (
            sb.table("shops")
            .select("*")
            .eq("is_approved", False)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return r.data or []
    except Exception as e:
        logger.exception("list_pending_shops: %s", e)
        return []


def get_shop_by_owner_user_id(owner_user_id: str) -> dict[str, Any] | None:
    sb = get_supabase()
    try:
        r = (
            sb.table("shops")
            .select("*")
            .eq("owner_user_id", owner_user_id)
            .limit(1)
            .execute()
        )
        if r.data:
            return r.data[0]
    except Exception as e:
        logger.exception("get_shop_by_owner_user_id: %s", e)
    return None


def list_products_for_seller_shop(shop_id: str, limit: int = 50) -> list[dict[str, Any]]:
    sb = get_supabase()
    try:
        r = (
            sb.table("products")
            .select("*")
            .eq("shop_id", shop_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return r.data or []
    except Exception as e:
        logger.exception("list_products_for_seller_shop: %s", e)
        return []


def set_product_active_for_shop(product_id: str, shop_id: str, active: bool) -> bool:
    sb = get_supabase()
    try:
        sb.table("products").update({"is_active": active}).eq("id", product_id).eq(
            "shop_id", shop_id
        ).execute()
        return True
    except Exception as e:
        logger.exception("set_product_active_for_shop: %s", e)
        return False


def shop_owned_by(shop_id: str, owner_user_uuid: str) -> bool:
    shop = get_shop_by_id(shop_id)
    if not shop:
        return False
    return str(shop.get("owner_user_id") or "") == owner_user_uuid


def get_or_create_user_by_telegram_id_only(
    telegram_id: int,
    username: str | None = None,
) -> dict[str, Any] | None:
    """Admin: sotuvchi uchun minimal foydalanuvchi."""
    return ensure_seller_user_for_admin(telegram_id, username)


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
