# Applications

module "pretix" {
  source = "./pretix"

  database_password = var.database_password
  mail_user         = var.mail_user
  mail_password     = var.mail_password
  secret_key        = var.pretix_secret_key
  sentry_dsn        = var.sentry_dsn
  ssl_certificate   = var.ssl_certificate
}

# Other resources

module "database" {
  source = "./database"

  database_password = var.database_password
}
