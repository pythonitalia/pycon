variable "application" {}
variable "docker_repository_name" {
  default = ""
}
variable "docker_tag" {}
variable "role_arn" {}
variable "env_vars" {
  type    = map(string)
  default = {}
}
variable "security_group_ids" {
  type    = list(string)
  default = []
}
variable "subnet_ids" {
  type    = list(string)
  default = []
}
