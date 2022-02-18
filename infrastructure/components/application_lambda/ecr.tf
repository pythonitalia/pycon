locals {
  image_uri_prefix = "${data.aws_caller_identity.current.account_id}.dkr.ecr.eu-central-1.amazonaws.com"
  repository_name  = "pythonit/${var.docker_repository_name != "" ? var.docker_repository_name : var.application}"
  image_uri        = "${local.image_uri_prefix}/${local.repository_name}:${data.external.githash.result.githash}"
}

data "aws_caller_identity" "current" {}

data "external" "githash" {
  program     = ["python", abspath("${path.module}/githash.py")]
  working_dir = abspath("${path.root}/../../${var.local_path == null ? var.application : var.local_path}")
}
