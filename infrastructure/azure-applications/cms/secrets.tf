data "azurerm_key_vault_secret" "db_username" {
  name         = "db-username"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  key_vault_id = azurerm_key_vault.vault.id
}
