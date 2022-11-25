data "azurerm_key_vault_secret" "secret_key" {
  name         = "secret-key"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "pastaporto_secret" {
  name         = "pastaporto-secret"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "identity_secret" {
  name         = "identity-secret"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "service_to_service_secret" {
  name         = "service-to-service-secret"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "db_username" {
  name         = "db-username"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  key_vault_id = azurerm_key_vault.vault.id
}
