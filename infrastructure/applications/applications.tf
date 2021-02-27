# Applications

module "pretix" {
  source = "./pretix"

  database_password = var.database_password
  mail_user         = var.mail_user
  mail_password     = var.mail_password
  secret_key        = var.pretix_secret_key
  sentry_dsn        = var.pretix_sentry_dsn
  ssl_certificate   = var.ssl_certificate
}

module "pycon_backend" {
  source = "./pycon_backend"

  database_password                = var.database_password
  secret_key                       = var.secret_key
  mapbox_public_api_key            = var.mapbox_public_api_key
  sentry_dsn                       = var.sentry_dsn
  slack_incoming_webhook_url       = var.slack_incoming_webhook_url
  social_auth_google_oauth2_key    = var.social_auth_google_oauth2_key
  social_auth_google_oauth2_secret = var.social_auth_google_oauth2_secret
  pretix_api_token                 = var.pretix_api_token
  pinpoint_application_id          = var.pinpoint_application_id
  ssl_certificate                  = var.ssl_certificate
}

# Other resources

module "database" {
  source = "./database"

  database_password = var.database_password
}
