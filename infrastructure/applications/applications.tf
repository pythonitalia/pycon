locals {
  is_prod         = terraform.workspace == "production"
  deploy_pretix   = local.is_prod
  deploy_temporal = false
  enable_proxy    = local.is_prod ? false : false
}

# Applications

module "pretix" {
  source       = "./pretix"
  count        = local.deploy_pretix ? 1 : 0
  enable_proxy = local.enable_proxy
}

module "temporal" {
  source       = "./temporal"
  count        = local.deploy_temporal ? 1 : 0
  enable_proxy = local.enable_proxy
}

module "pycon_backend" {
  source          = "./pycon_backend"
  enable_proxy    = local.enable_proxy
  deploy_temporal = local.deploy_temporal

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "gateway" {
  source = "./gateway"

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "users_backend" {
  source       = "./users_backend"
  depends_on   = [module.database]
  enable_proxy = local.enable_proxy
}

module "association_backend" {
  source       = "./association_backend"
  depends_on   = [module.database]
  enable_proxy = local.enable_proxy
}

module "email_templates" {
  source = "./email_templates"
}

# Other resources

module "database" {
  source       = "./database"
  enable_proxy = local.enable_proxy
}
