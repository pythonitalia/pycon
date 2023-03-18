resource "azurerm_private_dns_zone" "dns" {
  name                = "${var.workspace}.internaldns.python.it"
  resource_group_name = var.resource_group_name
}
