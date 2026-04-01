export type SubscriptionType = "free" | "pro" | "vip";

export interface Shop {
  id: string;
  name: string;
  description: string | null;
  owner_telegram_username: string | null;
  city: string | null;
  logo_url: string | null;
  banner_url: string | null;
  subscription_type: SubscriptionType | null;
  is_featured: boolean | null;
  created_at?: string;
}

export interface Product {
  id: string;
  name: string;
  description: string | null;
  price: number | null;
  image_url: string | null;
  category: string | null;
  shop_id: string;
  is_active: boolean | null;
  created_at?: string;
  shops?: Shop | null;
}
