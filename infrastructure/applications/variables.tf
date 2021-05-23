variable "ssl_certificate" {}
variable "mail_user" {}
variable "mail_password" {}
variable "pretix_secret_key" {}
variable "database_password" {}
variable "secret_key" {}
variable "mapbox_public_api_key" {}
variable "sentry_dsn" {}
variable "slack_incoming_webhook_url" {}
variable "social_auth_google_oauth2_key" {}
variable "social_auth_google_oauth2_secret" {}
variable "pretix_api_token" {}
variable "pinpoint_application_id" {}
variable "pretix_sentry_dsn" {}
variable "stripe_secret_api_key" {}

# Gateway secrets
variable "gateway_sentry_dsn" {}

# Users backend secrets
variable "users_backend_secret_key" {}
variable "users_backend_sentry_dsn" {}

# Association backend secrets
variable "association_backend_stripe_membership_price_id" {}
variable "association_backend_stripe_webhook_secret" {}
variable "association_backend_sentry_dsn" {}

# Secrets
variable "pastaporto_secret" {}
variable "identity_secret" {}
variable "service_to_service_secret" {}
variable "pastaporto_action_secret" {}
