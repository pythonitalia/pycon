variable "application" {}
variable "lambda_invoke_arn" {}
variable "lambda_function_name" {}
variable "use_domain" {
  type    = bool
  default = false
}
variable "zone_name" {
  default = ""
}
variable "domain" {
  default = ""
}
variable "certificate_arn" {
  default = ""
}
