locals {
  services = [
    "pycon-backend",
    "users-backend",
    "gateway"
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

resource "aws_ecr_lifecycle_policy" "service_repo_cleanup" {
  for_each   = toset(local.services)
  repository = aws_ecr_repository.service_repo[each.key].name
  policy     = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Expire untagged images older than 1 days",
            "selection": {
                "tagStatus": "untagged",
                "countType": "sinceImagePushed",
                "countUnit": "days",
                "countNumber": 1
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}
