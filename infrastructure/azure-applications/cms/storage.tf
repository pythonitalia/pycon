resource "azurerm_storage_account" "storage" {
  name                     = "${var.workspace}pythonitcms"
  resource_group_name      = var.resource_group_name
  location                 = var.resource_group_location
  account_tier             = "Standard"
  account_replication_type = "ZRS"
  min_tls_version          = "TLS1_2"
}

resource "azurerm_storage_container" "media" {
  name                  = "media"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "staticfiles" {
  name                  = "staticfiles"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "blob"
}
