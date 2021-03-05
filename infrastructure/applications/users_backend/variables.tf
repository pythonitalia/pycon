variable "jwt_auth_secret" {}
variable "session_secret_key" {}
variable "google_auth_client_id" {}
variable "google_auth_client_secret" {}
variable "database_password" {}

variable "pastaporto_secret" {}
variable "identity_secret" {}
variable "service_to_service_secret" {}

locals {
  application = "users-backend"
  domain_name = "users-api"
}
