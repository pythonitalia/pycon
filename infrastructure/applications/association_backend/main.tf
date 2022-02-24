locals {
  is_prod = terraform.workspace == "production"
  domain  = local.is_prod ? "${local.domain_name}.python.it" : "${terraform.workspace}-${local.domain_name}.python.it"

  # TODO: Need to coordinate between env and vercel
  association_frontend_url = "https://associazione.python.it"
  users_backend_url        = local.is_prod ? "https://users-api.python.it" : "https://${terraform.workspace}-users-api.python.it"

  db_connection = local.is_prod ? "postgresql://${data.aws_db_instance.database.master_username}:${module.common_secrets.value.database_password}@${data.aws_db_proxy.proxy[0].endpoint}:${data.aws_db_instance.database.port}/association" : "postgresql://${data.aws_db_instance.database.master_username}:${module.common_secrets.value.database_password}@${data.aws_db_instance.database.address}:${data.aws_db_instance.database.port}/association"
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

data "aws_db_proxy" "proxy" {
  count = local.is_prod ? 1 : 0
  name  = "pythonit-${terraform.workspace}-database-proxy"
}

module "lambda" {
  source = "../../components/application_lambda"

  application        = local.application
  role_arn           = data.aws_iam_role.lambda.arn
  subnet_ids         = [for subnet in data.aws_subnet_ids.private.ids : subnet]
  security_group_ids = [data.aws_security_group.rds.id, data.aws_security_group.lambda.id]
  env_vars = {
    DEBUG        = "false"
    DATABASE_URL = local.db_connection
    SENTRY_DSN   = module.secrets.value.sentry_dsn

    # Services
    ASSOCIATION_FRONTEND_URL = local.association_frontend_url
    USERS_SERVICE            = local.users_backend_url

    PRETIX_API       = "https://tickets.pycon.it/api/v1/"
    PRETIX_API_TOKEN = module.common_secrets.value.pretix_api_token

    # Secrets
    STRIPE_WEBHOOK_SIGNATURE_SECRET = module.secrets.value.stripe_webhook_secret
    STRIPE_SUBSCRIPTION_PRICE_ID    = module.secrets.value.stripe_membership_price_id
    STRIPE_SECRET_API_KEY           = module.secrets.value.stripe_secret_api_key
    PASTAPORTO_SECRET               = module.common_secrets.value.pastaporto_secret
    SERVICE_TO_SERVICE_SECRET       = module.common_secrets.value.service_to_service_secret
    PRETIX_WEBHOOK_SECRET           = module.secrets.value.pretix_webhook_secret
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
