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

data "aws_instance" "redis" {
  instance_tags = {
    Name = "pythonit-production-redis"
  }

  filter {
    name   = "instance-state-name"
    values = ["running"]
  }
}

data "aws_sesv2_configuration_set" "main" {
  configuration_set_name = "pythonit-${terraform.workspace}"
}

module "lambda" {
  source = "../../components/application_lambda"

  application        = local.application
  local_path         = local.local_path
  role_arn           = data.aws_iam_role.lambda.arn
  subnet_ids         = [for subnet in data.aws_subnets.private.ids : subnet]
  security_group_ids = [data.aws_security_group.rds.id, data.aws_security_group.lambda.id]
  env_vars = {
    DATABASE_URL                              = local.db_connection
    DEBUG                                     = "False"
    SECRET_KEY                                = module.secrets.value.secret_key
    MAPBOX_PUBLIC_API_KEY                     = module.secrets.value.mapbox_public_api_key
    SENTRY_DSN                                = module.secrets.value.sentry_dsn
    VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN     = module.secrets.value.volunteers_push_notifications_ios_arn
    VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN = module.secrets.value.volunteers_push_notifications_android_arn
    ALLOWED_HOSTS                             = ".pycon.it"
    DJANGO_SETTINGS_MODULE                    = "pycon.settings.prod"
    ASSOCIATION_FRONTEND_URL                  = "https://associazione.python.it"
    AWS_MEDIA_BUCKET                          = aws_s3_bucket.backend_media.id
    AWS_REGION_NAME                           = aws_s3_bucket.backend_media.region
    SPEAKERS_EMAIL_ADDRESS                    = module.secrets.value.speakers_email_address
    EMAIL_BACKEND                             = "django_ses.SESBackend"
    FRONTEND_URL                              = "https://pycon.it"
    PRETIX_API                                = "https://tickets.pycon.it/api/v1/"
    AWS_S3_CUSTOM_DOMAIN                      = local.cdn_url
    PRETIX_API_TOKEN                          = module.common_secrets.value.pretix_api_token
    MAILCHIMP_SECRET_KEY                      = module.common_secrets.value.mailchimp_secret_key
    MAILCHIMP_DC                              = module.common_secrets.value.mailchimp_dc
    MAILCHIMP_LIST_ID                         = module.common_secrets.value.mailchimp_list_id
    USER_ID_HASH_SALT                         = module.secrets.value.userid_hash_salt
    PLAIN_API                                 = "https://core-api.uk.plain.com/graphql/v1"
    PLAIN_API_TOKEN                           = module.secrets.value.plain_api_token
    CACHE_URL                                 = local.is_prod ? "redis://${data.aws_instance.redis.private_ip}/8" : "redis://${data.aws_instance.redis.private_ip}/13"
    STRIPE_WEBHOOK_SIGNATURE_SECRET           = module.secrets.value.stripe_webhook_secret
    STRIPE_SUBSCRIPTION_PRICE_ID              = module.secrets.value.stripe_membership_price_id
    STRIPE_SECRET_API_KEY                     = module.secrets.value.stripe_secret_api_key
    PRETIX_WEBHOOK_SECRET                     = module.secrets.value.pretix_webhook_secret
    OPENAI_API_KEY                            = module.secrets.value.openai_api_key
    FLODESK_API_KEY                           = module.secrets.value.flodesk_api_key
    FLODESK_SEGMENT_ID                        = module.secrets.value.flodesk_segment_id
    CELERY_BROKER_URL                         = local.is_prod ? "redis://${data.aws_instance.redis.private_ip}/5" : "redis://${data.aws_instance.redis.private_ip}/14"
    CELERY_RESULT_BACKEND                     = local.is_prod ? "redis://${data.aws_instance.redis.private_ip}/6" : "redis://${data.aws_instance.redis.private_ip}/15"
    PLAIN_INTEGRATION_TOKEN                   = module.secrets.value.plain_integration_token
    HASHID_DEFAULT_SECRET_SALT                = module.secrets.value.hashid_default_secret_salt
    MEDIA_FILES_STORAGE_BACKEND = "pycon.storages.CustomS3Boto3Storage"
    SNS_WEBHOOK_SECRET = module.common_secrets.value.sns_webhook_secret
    AWS_SES_CONFIGURATION_SET = data.aws_sesv2_configuration_set.main.configuration_set_name
  }
}

module "admin_distribution" {
  source = "../../components/cloudfront"

  application                    = local.application
  zone_name                      = "pycon.it"
  domain                         = local.full_admin_domain
  certificate_arn                = data.aws_acm_certificate.cert.arn
  origin_url                     = module.lambda.cloudfront_friendly_lambda_url
  forward_host_header_lambda_arn = data.aws_lambda_function.forward_host_header.qualified_arn
}
