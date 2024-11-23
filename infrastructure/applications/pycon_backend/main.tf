locals {
  is_prod           = terraform.workspace == "production"
  admin_domain      = "admin"
  full_admin_domain = local.is_prod ? "${local.admin_domain}.pycon.it" : "${terraform.workspace}-${local.admin_domain}.pycon.it"
  db_connection     = "postgres://${data.aws_db_instance.database.master_username}:${module.common_secrets.value.database_password}@${data.aws_db_instance.database.address}:${data.aws_db_instance.database.port}/pycon"
  cdn_url           = local.is_prod ? "cdn.pycon.it" : "${terraform.workspace}-cdn.pycon.it"
}

data "aws_vpc" "default" {
  filter {
    name   = "tag:Name"
    values = ["pythonit-vpc"]
  }
}

data "aws_iam_role" "lambda" {
  name = "pythonit-lambda-role"
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

data "aws_security_group" "rds" {
  name = "pythonit-rds-security-group"
}

data "aws_security_group" "lambda" {
  name = "pythonit-lambda-security-group"
}

data "aws_db_instance" "database" {
  db_instance_identifier = "pythonit-${terraform.workspace}"
}

data "aws_acm_certificate" "cert" {
  domain   = "*.pycon.it"
  statuses = ["ISSUED"]
  provider = aws.us
}

data "aws_lambda_function" "forward_host_header" {
  function_name = "forward_host_header"
  provider      = aws.us
}

data "aws_sesv2_configuration_set" "main" {
  configuration_set_name = "pythonit-${terraform.workspace}"
}
