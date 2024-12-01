resource "aws_ecr_repository" "repo" {
  name = "pythonit/${terraform.workspace}-pycon-frontend"
}

data "aws_ecr_image" "image" {
  repository_name = data.aws_ecr_repository.repo.name
  image_tag       = data.external.githash.result.githash
}

data "aws_caller_identity" "current" {}

data "external" "githash" {
  program     = ["python", abspath("${path.module}/../pretix/githash.py")]
  working_dir = abspath("${path.root}/../../frontend")
}
