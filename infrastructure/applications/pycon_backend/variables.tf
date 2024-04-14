locals {
  application = "pycon-backend"
  domain_name = "pycon-backend"
  local_path  = "backend"
}

variable "enable_proxy" {}
variable "ecs_arm_ami" {}
