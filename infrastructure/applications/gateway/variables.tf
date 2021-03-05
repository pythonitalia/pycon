variable "pastaporto_secret" {}
variable "identity_secret" {}
variable "service_to_service_secret" {}

locals {
  application = "gateway"
  domain_name = "beri"
}
