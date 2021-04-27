variable "database_password" {}
variable "pastaporto_secret" {}
variable "stripe_secret_api_key" {}
variable "stripe_subscription_price_id" {}
variable "stripe_webhook_secret" {}

locals {
  application = "association-backend"
  domain_name = "association-api"
}
