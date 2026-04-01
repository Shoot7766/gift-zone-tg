/** /api/me javobidagi rol manbasi */
export type RoleSource =
  | "database"
  | "admin_env"
  | "fallback_no_service_key"
  | "fallback_no_user_row"
  | "no_telegram_auth"
  | "missing_bot_token"
  | "invalid_init_data"
  | "server_error";
