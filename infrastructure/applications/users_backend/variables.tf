variable "jwt_auth_secret" {}
variable "session_secret_key" {}
variable "google_auth_client_id" {}
variable "google_auth_client_secret" {}
variable "database_password" {}

locals {
  application = "users-backend"
  domain_name = "users-api"
}
