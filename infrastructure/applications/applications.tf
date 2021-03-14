locals {
  deploy_pretix = terraform.workspace == "production"
}

# Applications

module "pretix" {
  source = "./pretix"
  count  = local.deploy_pretix ? 1 : 0

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

module "gateway" {
  source = "./gateway"

  pastaporto_secret         = var.pastaporto_secret
  identity_secret           = var.identity_secret
  service_to_service_secret = var.service_to_service_secret
  pastaporto_action_secret  = var.pastaporto_action_secret

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "admin_gateway" {
  source = "./gateway"

  pastaporto_secret         = var.pastaporto_secret
  identity_secret           = var.identity_secret
  service_to_service_secret = var.service_to_service_secret
  pastaporto_action_secret  = var.pastaporto_action_secret
  admin_variant             = true

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "users_backend" {
  source = "./users_backend"

  session_secret_key        = var.users_backend_session_secret_key
  google_auth_client_id     = var.social_auth_google_oauth2_key
  google_auth_client_secret = var.social_auth_google_oauth2_secret
  database_password         = var.database_password
  pastaporto_secret         = var.pastaporto_secret
  identity_secret           = var.identity_secret
  service_to_service_secret = var.service_to_service_secret
  pastaporto_action_secret  = var.pastaporto_action_secret

  depends_on = [module.database]
}

# Other resources

module "database" {
  source = "./database"

  database_password = var.database_password
}
