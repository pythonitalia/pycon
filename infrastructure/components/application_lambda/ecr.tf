locals {
  image_uri_prefix = "${data.aws_caller_identity.current.account_id}.dkr.ecr.eu-central-1.amazonaws.com"
  repository_name  = "pythonit/${var.docker_repository_name != "" ? var.docker_repository_name : var.application}"
  image_uri        = "${local.image_uri_prefix}/${local.repository_name}@${data.aws_ecr_image.image.image_digest}"
}

data "aws_caller_identity" "current" {}

data "aws_ecr_image" "image" {
  repository_name = local.repository_name
  image_tag       = var.docker_tag
}
