locals {
  backend_image_uri = "${data.aws_caller_identity.current.account_id}.dkr.ecr.eu-central-1.amazonaws.com/${aws_ecr_repository.backend_image.name}@${data.aws_ecr_image.backend_image.image_digest}"
}

resource "aws_ecr_repository" "backend_image" {
  name                 = "${terraform.workspace}-pycon-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "aws_ecr_lifecycle_policy" "backend_image_cleanup" {
  repository = aws_ecr_repository.backend_image.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Expire images older than 1 days",
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

data "aws_ecr_image" "backend_image" {
  repository_name = aws_ecr_repository.backend_image.name
  image_tag       = "latest"
  depends_on      = [aws_ecr_repository.backend_image]
}
