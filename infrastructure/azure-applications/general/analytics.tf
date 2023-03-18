resource "azurerm_log_analytics_workspace" "analytics" {
  name                = "pythonit-${var.workspace}-analytics"
  resource_group_name = var.resource_group_name
  location            = "westeurope"
  sku                 = "PerGB2018"
  retention_in_days   = 30
}
