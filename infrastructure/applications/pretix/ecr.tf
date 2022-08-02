data "aws_ecr_repository" "repo" {
  name = "pythonit/pretix"
}

data "aws_ecr_image" "image" {
  repository_name = data.aws_ecr_repository.repo.name
  image_tag       = data.external.githash.result.githash
}

data "aws_caller_identity" "current" {}

data "external" "githash" {
  program     = ["python", abspath("${path.module}/githash.py")]
  working_dir = abspath("${path.root}/../../pretix")
}
