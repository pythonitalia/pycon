locals {
  services = [
    "pycon-backend",
    "pycon-backend/cache",
    "pycon-frontend",
    "pycon-frontend/cache",
    "pretix",
    "pretix/cache",
  ]
  infrastructure_tools_account_id = [
    for account in data.aws_organizations_organization.organization.non_master_accounts :
    account.id
    if account.name == "Infrastructure Tools"
  ][0]
}

data "aws_organizations_organization" "organization" {}

resource "aws_ecr_repository" "service_repo" {
  for_each             = toset(local.services)
  name                 = "pythonit/${each.key}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

data "aws_iam_policy_document" "access_from_infrastructure_account" {
  statement {
    sid    = "access from infrastructure account"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [local.infrastructure_tools_account_id]
    }

    actions = [
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:BatchCheckLayerAvailability",
      "ecr:PutImage",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:DescribeRepositories",
      "ecr:GetRepositoryPolicy",
      "ecr:ListImages",
      "ecr:BatchDeleteImage",
    ]
  }
}

resource "aws_ecr_repository_policy" "access_from_infrastructure_account" {
  for_each             = toset(local.services)
  repository = aws_ecr_repository.service_repo[each.key].name
  policy     = data.aws_iam_policy_document.access_from_infrastructure_account.json
}
