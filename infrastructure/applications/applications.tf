locals {
  deploy_pretix = terraform.workspace == "production"
}

# Applications

module "pretix" {
  source = "./pretix"
  count  = local.deploy_pretix ? 1 : 0

  mail_user         = var.mail_user
  mail_password     = var.mail_password
  secret_key        = var.pretix_secret_key
  sentry_dsn        = var.pretix_sentry_dsn
  ssl_certificate   = var.ssl_certificate
  pretix_sentry_dsn = var.pretix_sentry_dsn
}

module "pycon_backend" {
  source = "./pycon_backend"

  ssl_certificate = var.ssl_certificate
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
