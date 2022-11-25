data "azurerm_key_vault_secret" "root_username" {
  name         = "db-root-username"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "root_password" {
  name         = "db-root-password"
  key_vault_id = azurerm_key_vault.vault.id
}
