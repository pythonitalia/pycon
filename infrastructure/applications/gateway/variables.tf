variable "pastaporto_secret" {}
variable "identity_secret" {}
variable "service_to_service_secret" {}
variable "pastaporto_action_secret" {}
variable "admin_variant" {
  type    = bool
  default = false
}

locals {
  application = var.admin_variant ? "admin-gateway" : "gateway"
  domain_name = var.admin_variant ? "admin-beri" : "beri"
}
