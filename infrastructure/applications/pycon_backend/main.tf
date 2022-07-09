locals {
  is_prod                 = terraform.workspace == "production"
  admin_domain            = "admin"
  full_admin_domain       = local.is_prod ? "${local.admin_domain}.pycon.it" : "${terraform.workspace}-${local.admin_domain}.pycon.it"
  users_backend_url       = local.is_prod ? "https://users-api.python.it" : "https://${terraform.workspace}-users-api.python.it"
  association_backend_url = local.is_prod ? "https://association-api.python.it" : "https://${terraform.workspace}-association-api.python.it"
  db_connection           = var.enable_proxy ? "postgres://${data.aws_db_instance.database.master_username}:${module.common_secrets.value.database_password}@${data.aws_db_proxy.proxy[0].endpoint}:${data.aws_db_instance.database.port}/${data.aws_db_instance.database.db_name}" : "postgres://${data.aws_db_instance.database.master_username}:${module.common_secrets.value.database_password}@${data.aws_db_instance.database.address}:${data.aws_db_instance.database.port}/${data.aws_db_instance.database.db_name}"
  cdn_url                 = local.is_prod ? "cdn.pycon.it" : "${terraform.workspace}-cdn.pycon.it"
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

data "aws_db_proxy" "proxy" {
  count = var.enable_proxy ? 1 : 0
  name  = "pythonit-${terraform.workspace}-database-proxy"
}

data "aws_acm_certificate" "cert" {
  domain   = "*.pycon.it"
  statuses = ["ISSUED"]
  provider = aws.us
}

module "lambda" {
  source = "../../components/application_lambda"

  application        = local.application
  local_path         = local.local_path
  role_arn           = data.aws_iam_role.lambda.arn
  subnet_ids         = [for subnet in data.aws_subnet_ids.private.ids : subnet]
  security_group_ids = [data.aws_security_group.rds.id, data.aws_security_group.lambda.id]
  architecture       = "arm64"
  env_vars = {
    DATABASE_URL                                  = local.db_connection
    DEBUG                                         = "False"
    SECRET_KEY                                    = module.secrets.value.secret_key
    MAPBOX_PUBLIC_API_KEY                         = module.secrets.value.mapbox_public_api_key
    SENTRY_DSN                                    = module.secrets.value.sentry_dsn
    CFP_SLACK_INCOMING_WEBHOOK_URL                = module.secrets.value.cfp_slack_incoming_webhook_url
    SUBMISSION_COMMENT_SLACK_INCOMING_WEBHOOK_URL = module.secrets.value.submission_comment_slack_incoming_webhook_url
    VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN         = module.secrets.value.volunteers_push_notifications_ios_arn
    VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN     = module.secrets.value.volunteers_push_notifications_android_arn
    ALLOWED_HOSTS                                 = "*"
    DJANGO_SETTINGS_MODULE                        = "pycon.settings.prod"
    AWS_MEDIA_BUCKET                              = aws_s3_bucket.backend_media.id
    AWS_REGION_NAME                               = aws_s3_bucket.backend_media.region
    SPEAKERS_EMAIL_ADDRESS                        = module.secrets.value.speakers_email_address
    EMAIL_BACKEND                                 = "django_ses.SESBackend"
    PYTHONIT_EMAIL_BACKEND                        = "pythonit_toolkit.emails.backends.ses.SESEmailBackend"
    FRONTEND_URL                                  = "https://pycon.it"
    PRETIX_API                                    = "https://tickets.pycon.it/api/v1/"
    AWS_S3_CUSTOM_DOMAIN                          = local.cdn_url
    PRETIX_API_TOKEN                              = module.common_secrets.value.pretix_api_token
    PINPOINT_APPLICATION_ID                       = module.secrets.value.pinpoint_application_id
    PASTAPORTO_SECRET                             = module.common_secrets.value.pastaporto_secret
    FORCE_PYCON_HOST                              = local.is_prod
    ASSOCIATION_BACKEND_SERVICE                   = local.association_backend_url
    USERS_SERVICE                                 = local.users_backend_url
    SERVICE_TO_SERVICE_SECRET                     = module.common_secrets.value.service_to_service_secret
    SQS_QUEUE_URL                                 = aws_sqs_queue.queue.id
    MAILCHIMP_SECRET_KEY                          = module.common_secrets.value.mailchimp_secret_key
    MAILCHIMP_DC                                  = module.common_secrets.value.mailchimp_dc
    MAILCHIMP_LIST_ID                             = module.common_secrets.value.mailchimp_list_id
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
