data "azurerm_client_config" "current" {}

data "azurerm_key_vault" "staging_db_vault" {
  name                = "staging-database"
  resource_group_name = "pythonitalia-staging"
}

resource "azurerm_user_assigned_identity" "anonymizer" {
  resource_group_name = azurerm_resource_group.anonymizer.name
  location            = azurerm_resource_group.anonymizer.location
  name                = "anonymizer"
}

resource "azurerm_role_assignment" "db_staging_read_vault" {
  scope                = data.azurerm_key_vault.staging_db_vault.id
  role_definition_name = "Reader"
  principal_id         = azurerm_user_assigned_identity.anonymizer.principal_id
}

resource "azurerm_role_assignment" "storage" {
  scope                = azurerm_storage_account.storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.anonymizer.principal_id
}

resource "azurerm_key_vault_access_policy" "db_staging_permissions" {
  key_vault_id = data.azurerm_key_vault.staging_db_vault.id
  tenant_id    = azurerm_user_assigned_identity.anonymizer.tenant_id
  object_id    = azurerm_user_assigned_identity.anonymizer.principal_id

  key_permissions = [
    "Get",
  ]

  secret_permissions = [
    "Get",
  ]
}
