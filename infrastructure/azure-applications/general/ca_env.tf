locals {
  cms = var.is_prod ? "cms.python.it" : "${var.workspace}-cms.python.it"
  apps_domains = [
    local.cms,
  ]
}

resource "azurerm_container_app_environment" "env" {
  name                       = "pythonit-${var.workspace}-env"
  location                   = "westeurope"
  resource_group_name        = azurerm_resource_group.pythonitalia.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.analytics.id
  infrastructure_subnet_id   = azurerm_subnet.apps.id
}

data "azapi_resource" "env" {
  type                   = "Microsoft.App/managedEnvironments@2022-10-01"
  resource_id            = data.azurerm_container_app_environment.env.id
  response_export_values = ["properties.customDomainConfiguration.customDomainVerificationId"]
}

resource "aws_route53_record" "txt_verification" {
  for_each = local.apps_domains

  zone_id = data.aws_route53_zone.zone.zone_id
  name    = "asuid.${each.key}"
  type    = "TXT"
  ttl     = "30"
  records = [jsondecode(data.azapi_resource.env.output).properties.customDomainConfiguration.customDomainVerificationId]
}
