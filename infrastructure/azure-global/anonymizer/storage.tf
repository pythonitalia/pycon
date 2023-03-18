resource "azurerm_storage_account" "storage" {
  name                     = "pythonitanonymizeddb"
  resource_group_name      = azurerm_resource_group.anonymizer.name
  location                 = azurerm_resource_group.anonymizer.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
}

resource "azurerm_storage_container" "data" {
  name                  = "data"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}
