module "general" {
  source = "./general"

  is_prod                 = local.is_prod
  workspace               = local.workspace
  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location
}

module "database" {
  source = "./database"

  is_prod                 = local.is_prod
  workspace               = local.workspace
  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location
}

module "pycon_backend" {
  source = "./pycon_backend"

  is_prod                 = local.is_prod
  workspace               = local.workspace
  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location
  githash                 = var.githash_pycon_backend
}

module "users_backend" {
  source = "./users_backend"

  is_prod                 = local.is_prod
  workspace               = local.workspace
  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location
  githash                 = var.githash_users_backend
}
