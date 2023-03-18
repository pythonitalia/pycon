resource "azurerm_postgresql_flexible_server" "database" {
  name                = "pythonit-${var.workspace}-database"
  location            = "westeurope"
  resource_group_name = var.resource_group_name
  zone                = "3"

  sku_name = "B_Standard_B1ms"

  storage_mb                   = 32768
  backup_retention_days        = 7
  geo_redundant_backup_enabled = var.is_prod

  private_dns_zone_id = azurerm_private_dns_zone.dns.id
  delegated_subnet_id = data.azurerm_subnet.db_subnet.id

  administrator_login    = data.azurerm_key_vault_secret.root_username.value
  administrator_password = data.azurerm_key_vault_secret.root_password.value
  version                = "14"
  depends_on = [
    azurerm_private_dns_zone_virtual_network_link.db_link
  ]
}
