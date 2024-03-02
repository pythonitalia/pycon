locals {
  image_uri_prefix   = "${data.aws_caller_identity.current.account_id}.dkr.ecr.eu-central-1.amazonaws.com"
  pycon_be_image_uri = "${local.image_uri_prefix}/pythonit/pycon-backend:${data.external.githash_pycon_be.result.githash}"
}

data "aws_caller_identity" "current" {}

data "external" "githash_pycon_be" {
  program     = ["python", abspath("${path.module}/githash.py")]
  working_dir = abspath("${path.root}/../../backend")
}
