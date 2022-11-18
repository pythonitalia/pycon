module "general" {
  source = "./general"

  is_prod             = local.is_prod
  workspace           = local.workspace
  resource_group_name = local.resource_group_name
}

module "pycon_backend" {
  source     = "./pycon_backend"
  depends_on = [module.general]

  is_prod             = local.is_prod
  workspace           = local.workspace
  resource_group_name = local.resource_group_name
}
