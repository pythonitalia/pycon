locals {
  resource_group_name     = "pythonit-global"
  resource_group_location = "germanywestcentral"
}

module "ad" {
  source = "./ad"
}

module "resource_group" {
  source = "./resource_group"

  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location
}

module "vnet" {
  source = "./vnet"

  resource_group_name = local.resource_group_name
}

module "anonymizer" {
  source = "./anonymizer"

  resource_group_name = local.resource_group_name
}

module "certificates" {
  source = "./certificates"

  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location
}
