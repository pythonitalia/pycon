variable "admin_variant" {
  type    = bool
  default = false
}

locals {
  application = var.admin_variant ? "admin-gateway" : "gateway"
  domain_name = var.admin_variant ? "admin-beri" : "beri"
}
