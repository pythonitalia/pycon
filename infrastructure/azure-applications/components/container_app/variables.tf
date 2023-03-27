variable "environment_name" {
  type = string
}

variable "service_name" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "env_vars" {
  type = list(object({
    name   = string
    value  = string
    secret = bool
  }))
}

variable "workspace" {
  type = string
}

variable "local_path" {
  type    = string
  default = null
}

variable "githash" {
  type = string
}

variable "command" {
  type    = list(string)
  default = null
}

variable "port" {
  type = number
}

variable "healthcheck_path" {
  type    = string
  default = "/graphql"
}

variable "domain" {
  type    = string
  default = null
}
