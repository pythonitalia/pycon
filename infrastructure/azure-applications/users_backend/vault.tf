data "azurerm_client_config" "current" {}
data "azuread_group" "devs" {
  display_name = "devs"
}

resource "azurerm_key_vault" "vault" {
  name                          = "${var.workspace}-users"
  location                      = "westeurope"
  resource_group_name           = var.resource_group_name
  tenant_id                     = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days    = 7
  purge_protection_enabled      = false
  public_network_access_enabled = true
  sku_name                      = "standard"
}

resource "azurerm_key_vault_access_policy" "current_tenant_policy" {
  key_vault_id = azurerm_key_vault.vault.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  key_permissions = [
    "Get",
  ]

  secret_permissions = [
    "Get",
  ]
}


resource "azurerm_key_vault_access_policy" "devs_policy" {
  key_vault_id = azurerm_key_vault.vault.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azuread_group.devs.object_id

  key_permissions = [
    "Get",
    "List",
    "Create",
    "Delete",
    "Update",
    "UnwrapKey",
    "Verify",
    "WrapKey",
    "Release",
    "Rotate",
  ]

  secret_permissions = [
    "Get",
    "List",
    "Delete",
    "Purge",
    "Set",
    "Restore",
    "Recover"
  ]
}
