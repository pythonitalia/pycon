locals {
  is_prod           = terraform.workspace == "production"
  admin_domain      = "admin"
  full_admin_domain = local.is_prod ? "${local.admin_domain}.pycon.it" : "${terraform.workspace}-${local.admin_domain}.pycon.it"
  users_backend_url = local.is_prod ? "https://users-api.python.it" : "https://${terraform.workspace}-users-api.python.it"
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

data "aws_subnet_ids" "private" {
  vpc_id = data.aws_vpc.default.id

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

module "lambda" {
  source = "../../components/application_lambda"

  application        = local.application
  docker_tag         = terraform.workspace
  role_arn           = data.aws_iam_role.lambda.arn
  subnet_ids         = [for subnet in data.aws_subnet_ids.private.ids : subnet]
  security_group_ids = [data.aws_security_group.rds.id, data.aws_security_group.lambda.id]
  env_vars = {
    DATABASE_URL                     = "postgres://${data.aws_db_instance.database.master_username}:${module.common_secrets.value.database_password}@${data.aws_db_instance.database.address}:${data.aws_db_instance.database.port}/${data.aws_db_instance.database.db_name}"
    DEBUG                            = "False"
    SECRET_KEY                       = module.secrets.value.secret_key
    MAPBOX_PUBLIC_API_KEY            = module.secrets.value.mapbox_public_api_key
    SENTRY_DSN                       = module.secrets.value.sentry_dsn
    SLACK_INCOMING_WEBHOOK_URL       = module.secrets.value.slack_incoming_webhook_url
    ALLOWED_HOSTS                    = "*"
    DJANGO_SETTINGS_MODULE           = "pycon.settings.prod"
    AWS_MEDIA_BUCKET                 = aws_s3_bucket.backend_media.id
    AWS_REGION_NAME                  = aws_s3_bucket.backend_media.region
    EMAIL_BACKEND                    = "django_ses.SESBackend"
    FRONTEND_URL                     = "https://pycon.it"
    PRETIX_API                       = "https://tickets.pycon.it/api/v1/"
    PRETIX_API_TOKEN                 = module.secrets.value.pretix_api_token
    PINPOINT_APPLICATION_ID          = module.secrets.value.pinpoint_application_id
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY    = module.secrets.value.google_oauth2_key
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = module.secrets.value.google_oauth2_secret
    PASTAPORTO_SECRET                = module.common_secrets.value.pastaporto_secret
    FORCE_PYCON_HOST                 = local.is_prod
    USERS_SERVICE                    = local.users_backend_url
    SERVICE_TO_SERVICE_SECRET        = module.common_secrets.value.service_to_service_secret
    SQS_QUEUE_URL                    = aws_sqs_queue.queue.id
  }
}


module "api" {
  source = "../../components/http_api_gateway"

  application          = local.application
  use_domain           = false
  lambda_invoke_arn    = module.lambda.invoke_arn
  lambda_function_name = module.lambda.function_name
}


module "admin_distribution" {
  source = "../../components/cloudfront"

  application     = local.application
  zone_name       = "pycon.it"
  domain          = local.full_admin_domain
  certificate_arn = data.aws_acm_certificate.cert.arn
  origin_url      = module.api.cloudfront_friendly_endpoint
}
