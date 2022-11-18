resource "azurerm_storage_account" "storage" {
  name                     = "${var.workspace}pyconbackend"
  resource_group_name      = data.azurerm_resource_group.pythonitalia.name
  location                 = data.azurerm_resource_group.pythonitalia.location
  account_tier             = "Standard"
  account_replication_type = "ZRS"
  min_tls_version          = "TLS1_2"

  blob_properties {
    cors_rule {
      allowed_headers    = ["*"]
      allowed_methods    = ["PUT", "POST"]
      allowed_origins    = var.is_prod ? ["https://pycon.it"] : ["*"]
      exposed_headers    = ["*"]
      max_age_in_seconds = 0
    }
  }
}

resource "azurerm_storage_container" "temporary_uploads" {
  name                  = "temporary-uploads"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "participants_avatars" {
  name                  = "participants-avatars"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "blob"
}

resource "azurerm_storage_management_policy" "policy" {
  storage_account_id = azurerm_storage_account.storage.id

  rule {
    name    = "delete unused temporary old files"
    enabled = true

    filters {
      prefix_match = ["${azurerm_storage_container.temporary_uploads.name}/"]
      blob_types   = ["blockBlob"]
    }

    actions {
      base_blob {
        delete_after_days_since_modification_greater_than = 1
      }
    }
  }
}
