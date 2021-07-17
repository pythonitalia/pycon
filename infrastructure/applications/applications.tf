locals {
  deploy_pretix = terraform.workspace == "production"
}

# Applications

module "pretix" {
  source = "./pretix"
  count  = local.deploy_pretix ? 1 : 0
}

module "pycon_backend" {
  source = "./pycon_backend"
}

module "gateway" {
  source = "./gateway"

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "admin_gateway" {
  source        = "./gateway"
  admin_variant = true

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "users_backend" {
  source     = "./users_backend"
  depends_on = [module.database]
}

module "association_backend" {
  source     = "./association_backend"
  depends_on = [module.database]
}

module "email_templates" {
  source = "./email_templates"
}

# Other resources

module "database" {
  source = "./database"
}
