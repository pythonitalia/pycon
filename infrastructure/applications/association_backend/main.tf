locals {
  is_prod = terraform.workspace == "production"
  domain  = local.is_prod ? "${local.domain_name}.python.it" : "${terraform.workspace}-${local.domain_name}.python.it"

  # TODO: Need to coordinate between env and vercel
  association_frontend_url = "https://associazione.python.it"
}

data "aws_db_instance" "database" {
  db_instance_identifier = "pythonit-${terraform.workspace}"
}

data "aws_iam_role" "lambda" {
  name = "pythonit-lambda-role"
}

data "aws_vpc" "default" {
  filter {
    name   = "tag:Name"
    values = ["pythonit-vpc"]
  }
}

data "aws_subnet_ids" "private" {
  vpc_id = data.aws_vpc.default.id

  tags = {
    Type = "private"
  }
}

data "aws_security_group" "lambda" {
  name = "pythonit-lambda-security-group"
}

data "aws_security_group" "rds" {
  name = "pythonit-rds-security-group"
}

module "lambda" {
  source = "../../components/application_lambda"

  application        = local.application
  docker_tag         = terraform.workspace
  role_arn           = data.aws_iam_role.lambda.arn
  subnet_ids         = [for subnet in data.aws_subnet_ids.private.ids : subnet]
  security_group_ids = [data.aws_security_group.rds.id, data.aws_security_group.lambda.id]
  env_vars = {
    DEBUG        = "false"
    DATABASE_URL = "postgresql://${data.aws_db_instance.database.master_username}:${var.database_password}@${data.aws_db_instance.database.address}:${data.aws_db_instance.database.port}/association"
    SENTRY_DSN   = var.sentry_dsn

    # Services
    ASSOCIATION_FRONTEND_URL = local.association_frontend_url

    # Secrets
    STRIPE_WEBHOOK_SIGNATURE_SECRET = var.stripe_webhook_secret
    STRIPE_SUBSCRIPTION_PRICE_ID    = var.stripe_subscription_price_id
    STRIPE_SECRET_API_KEY           = var.stripe_secret_api_key
    PASTAPORTO_SECRET               = var.pastaporto_secret
  }
}

data "aws_acm_certificate" "cert" {
  domain   = "*.python.it"
  statuses = ["ISSUED"]
}

module "api" {
  source = "../../components/http_api_gateway"

  application          = local.application
  use_domain           = true
  domain               = local.domain
  zone_name            = "python.it"
  certificate_arn      = data.aws_acm_certificate.cert.arn
  lambda_invoke_arn    = module.lambda.invoke_arn
  lambda_function_name = module.lambda.function_name
}
