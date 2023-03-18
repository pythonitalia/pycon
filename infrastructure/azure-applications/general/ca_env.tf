resource "azurerm_container_app_environment" "env" {
  name                       = "pythonit-${var.workspace}-env"
  location                   = "westeurope"
  resource_group_name        = azurerm_resource_group.pythonitalia.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.analytics.id
  infrastructure_subnet_id   = azurerm_subnet.apps.id
}
