data "azurerm_virtual_network" "vnet" {
  name                = "pythonit-westeurope-vnet"
  resource_group_name = var.resource_group_name
}

data "azurerm_resource_group" "global" {
  name = var.resource_group_name
}

data "azurerm_subnet" "subnet" {
  name                 = "tasks-subnet"
  virtual_network_name = data.azurerm_virtual_network.vnet.name
  resource_group_name  = var.resource_group_name
}

resource "azurerm_container_group" "restore_data_job" {
  name                = "anonymizer-restore-data-job"
  location            = azurerm_resource_group.anonymizer.location
  resource_group_name = azurerm_resource_group.anonymizer.name
  ip_address_type     = "Private"
  os_type             = "Linux"
  restart_policy      = "Never"
  subnet_ids          = [data.azurerm_subnet.subnet.id]

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.anonymizer.id]
  }

  container {
    name   = "main"
    image  = "pythonitalia/anonymizer:latest"
    cpu    = "1"
    memory = "1"
    commands = [
      "poetry", "run", "python", "main.py", "restore-azure-staging-local"
    ]
    environment_variables = {
      UPLOAD_SOURCE = "azure"
      BUCKET_NAME   = azurerm_storage_account.storage.name
    }
    ports {
      port     = 9999
      protocol = "TCP"
    }
  }
}
