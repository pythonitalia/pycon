data "aws_ecr_repository" "be_repo" {
  name = "pythonit/pycon-backend"
}

data "aws_ecr_image" "be_image" {
  repository_name = data.aws_ecr_repository.be_repo.name
  image_tag       = data.external.githash.result.githash
}

data "aws_caller_identity" "current" {}

data "external" "githash" {
  program     = ["python", abspath("${path.module}/../pretix/githash.py")]
  working_dir = abspath("${path.root}/../../backend")
}
