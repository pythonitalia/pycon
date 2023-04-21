data "azurerm_client_config" "current" {}
data "azuread_group" "devs" {
  display_name = "devs"
}

resource "azurerm_key_vault" "certs" {
  name                       = "pythonit-certs"
  location                   = var.resource_group_location
  resource_group_name        = var.resource_group_name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  sku_name                   = "standard"
}

resource "azurerm_key_vault_access_policy" "current_tenant_policy" {
  key_vault_id = azurerm_key_vault.certs.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  secret_permissions = [
    "Get",
  ]

  certificate_permissions = [
    "Create",
    "Delete",
    "DeleteIssuers",
    "Get",
    "GetIssuers",
    "Import",
    "List",
    "ListIssuers",
    "ManageContacts",
    "ManageIssuers",
    "SetIssuers",
    "Update",
    "Purge",
  ]
}

resource "azurerm_key_vault_access_policy" "devs_policy" {
  key_vault_id = azurerm_key_vault.certs.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azuread_group.devs.object_id

  certificate_permissions = [
    "Create",
    "Delete",
    "DeleteIssuers",
    "Get",
    "GetIssuers",
    "Import",
    "List",
    "ListIssuers",
    "ManageContacts",
    "ManageIssuers",
    "SetIssuers",
    "Update",
    "Purge"
  ]
}

resource "azurerm_key_vault_certificate" "pythonit_cert" {
  name         = "pythonit"
  key_vault_id = azurerm_key_vault.certs.id

  certificate {
    contents = acme_certificate.python_it.certificate_p12
    password = ""
  }
}

resource "azurerm_key_vault_certificate" "pyconit_cert" {
  name         = "pyconit"
  key_vault_id = azurerm_key_vault.certs.id

  certificate {
    contents = acme_certificate.pycon_it.certificate_p12
    password = ""
  }
}
