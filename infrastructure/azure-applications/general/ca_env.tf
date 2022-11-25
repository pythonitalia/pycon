data "azurerm_subnet" "apps_subnet" {
  name                 = "apps-subnet"
  virtual_network_name = "pythonit-westeurope-vnet"
  resource_group_name  = "pythonit-global"
}

resource "azurerm_container_app_environment" "env" {
  name                       = "pythonit-${var.workspace}-env"
  location                   = "westeurope"
  resource_group_name        = azurerm_resource_group.pythonitalia.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.analytics.id
  infrastructure_subnet_id   = data.azurerm_subnet.apps_subnet.id
}

resource "azapi_resource" "aca_env" {
  type      = "Microsoft.App/managedEnvironments@2022-03-01"
  parent_id = azurerm_resource_group.pythonitalia.id
  location  = "westeurope"
  name      = "pythonit-${var.workspace}-ca-env"

  body = jsonencode({
    properties = {
      vnetConfiguration = {
        runtimeSubnetId        = data.azurerm_subnet.apps_subnet.id
        infrastructureSubnetId = data.azurerm_subnet.apps_subnet.id
        internal               = false
      }
      appLogsConfiguration = {
        destination = "log-analytics"
        logAnalyticsConfiguration = {
          customerId = azurerm_log_analytics_workspace.analytics.workspace_id
          sharedKey  = azurerm_log_analytics_workspace.analytics.primary_shared_key
        }
      }
    }
  })
}
