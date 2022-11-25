locals {
  resource_group_name = "pythonit-global"
}

module "ad" {
  source = "./ad"
}

module "resource_group" {
  source = "./resource_group"

  resource_group_name = local.resource_group_name
}

module "vnet" {
  source = "./vnet"

  resource_group_name = local.resource_group_name
}

module "anonymizer" {
  source = "./anonymizer"

  resource_group_name = local.resource_group_name
}
