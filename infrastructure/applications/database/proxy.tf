data "aws_secretsmanager_secret" "credentials" {
  count = var.enable_proxy ? 1 : 0
  name  = "/pythonit/${terraform.workspace}/common/database"
}

data "aws_vpc" "default" {
  filter {
    name   = "tag:Name"
    values = ["pythonit-vpc"]
  }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }

  tags = {
    Type = "private"
  }
}


resource "aws_db_proxy" "proxy" {
  count                  = var.enable_proxy ? 1 : 0
  name                   = "pythonit-${terraform.workspace}-database-proxy"
  debug_logging          = false
  engine_family          = "POSTGRESQL"
  idle_client_timeout    = 1800
  require_tls            = false
  role_arn               = aws_iam_role.proxy_role[0].arn
  vpc_security_group_ids = [data.aws_security_group.rds.id]
  vpc_subnet_ids         = data.aws_subnets.private.ids

  auth {
    auth_scheme = "SECRETS"
    description = "auth"
    iam_auth    = "DISABLED"
    secret_arn  = data.aws_secretsmanager_secret.credentials[0].arn
  }
}

resource "aws_iam_role" "proxy_role" {
  count              = var.enable_proxy ? 1 : 0
  name               = "pythonit-${terraform.workspace}-proxy-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "rds.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "pretix" {
  count = var.enable_proxy ? 1 : 0
  name  = "pythonit-${terraform.workspace}-proxy-policy"
  role  = aws_iam_role.proxy_role[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["secretsmanager:GetSecretValue"]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_db_proxy_default_target_group" "proxy" {
  count         = var.enable_proxy ? 1 : 0
  db_proxy_name = aws_db_proxy.proxy[0].name
}


resource "aws_db_proxy_target" "proxy_target" {
  count                  = var.enable_proxy ? 1 : 0
  db_instance_identifier = aws_db_instance.database.id
  db_proxy_name          = aws_db_proxy.proxy[0].name
  target_group_name      = aws_db_proxy_default_target_group.proxy[0].name
}
