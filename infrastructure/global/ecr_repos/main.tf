locals {
  services = [
    "pycon-backend",
    "pycon-backend/cache",
    "pretix",
    "pretix/cache",
  ]
}


resource "aws_ecr_repository" "service_repo" {
  for_each             = toset(local.services)
  name                 = "pythonit/${each.key}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}
