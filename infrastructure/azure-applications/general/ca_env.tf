resource "azurerm_container_app_environment" "env" {
  name                       = "pythonit-${var.workspace}-env"
  location                   = "westeurope"
  resource_group_name        = azurerm_resource_group.pythonitalia.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.analytics.id
  infrastructure_subnet_id   = azurerm_subnet.apps.id
}

data "azurerm_key_vault" "certs" {
  name                = "pythonit-certs"
  resource_group_name = "pythonit-global"
}

data "azurerm_key_vault_certificate_data" "pythonit" {
  name         = "pythonit"
  key_vault_id = data.azurerm_key_vault.certs.id
}

resource "azurerm_container_app_environment_certificate" "pythonit" {
  name                         = "pythonit"
  container_app_environment_id = azurerm_container_app_environment.env.id
  certificate_blob_base64      = base64encode("${data.azurerm_key_vault_certificate_data.pythonit.pem}\n${data.azurerm_key_vault_certificate_data.pythonit.key}")
  certificate_password         = ""
}
