locals {
  application = "pycon-backend"
  domain_name = "pycon-backend"
  local_path  = "backend"
}

variable "cluster_id" {}
variable "security_group_id" {}
variable "server_ip" {}
variable "logs_group_name" {}
variable "iam_role_arn" {}
variable "database_settings" {}
variable "vpc_id" {}
