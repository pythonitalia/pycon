variable "application" {}
variable "docker_repository_name" {
  default = ""
}
variable "docker_tag" {
  default = null
}
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
variable "memory_size" {
  type    = number
  default = 512
}
variable "local_path" {
  default = null
}
