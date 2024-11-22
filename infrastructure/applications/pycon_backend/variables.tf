locals {
  application = "pycon-backend"
  domain_name = "pycon-backend"
  local_path  = "backend"
}

variable "ecs_arm_ami" {}
variable "cluster_id" {}
variable "service_connect_namespace" {}
variable "security_group_id" {}
variable "server_ip" {}
