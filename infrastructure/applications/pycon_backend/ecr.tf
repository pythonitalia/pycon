locals {
  repository_name   = "pythonit/pycon-backend"
  backend_image_uri = "${data.aws_caller_identity.current.account_id}.dkr.ecr.eu-central-1.amazonaws.com/${local.repository_name}@${data.aws_ecr_image.backend_image.image_digest}"
}

data "aws_caller_identity" "current" {}

data "aws_ecr_image" "backend_image" {
  repository_name = local.repository_name
  image_tag       = "production"
}
