data "azurerm_key_vault_secret" "db_username" {
  name         = "db-username"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "service_to_service_secret" {
  name         = "service-to-service-secret"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "sentry_dsn" {
  name         = "sentry-dsn"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "mapbox_public_api_key" {
  name         = "mapbox-public-api-key"
  key_vault_id = azurerm_key_vault.vault.id
}
