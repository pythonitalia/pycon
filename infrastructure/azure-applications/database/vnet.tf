data "azurerm_virtual_network" "vnet" {
  name                = "pythonit-westeurope-vnet"
  resource_group_name = "pythonit-global"
}

data "azurerm_subnet" "db_subnet" {
  name                 = "db-subnet"
  virtual_network_name = data.azurerm_virtual_network.vnet.name
  resource_group_name  = "pythonit-global"
}

resource "azurerm_private_dns_zone" "dns" {
  name                = "db.${var.workspace}.private.postgres.database.azure.com"
  resource_group_name = var.resource_group_name
}

resource "azurerm_private_dns_zone_virtual_network_link" "db_link" {
  name                  = "db"
  private_dns_zone_name = azurerm_private_dns_zone.dns.name
  virtual_network_id    = data.azurerm_virtual_network.vnet.id
  resource_group_name   = var.resource_group_name
}
