locals {
  database_url = "postgresql://${data.azurerm_key_vault_secret.db_username.value}:${data.azurerm_key_vault_secret.db_password.value}@${data.azurerm_postgresql_flexible_server.db.fqdn}:5432/pycon?sslmode=require"
  domain       = var.is_prod ? "azure-admin.pycon.it" : "${var.workspace}-admin.pycon.it"
  cdn_url      = local.is_prod ? "cdn.pycon.it" : "${var.workspace}-cdn.pycon.it"
}

resource "random_password" "secret_key" {
  length           = 512
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

data "azurerm_postgresql_flexible_server" "db" {
  name                = "pythonit-${var.workspace}-database"
  resource_group_name = var.resource_group_name
}

data "aws_sqs_queue" "queue" {
  name = "${var.workspace}-pycon-backend.fifo"
}

module "app" {
  source                = "../components/container_app"
  service_name          = "pycon-backend"
  service_resource_name = "pycon"
  resource_group_name   = var.resource_group_name
  workspace             = var.workspace
  githash               = var.githash
  environment_name      = "pythonit-${var.workspace}-env"
  healthcheck_path      = "/graphql"
  port                  = 8000
  domain                = local.domain
  command               = ["/home/app/.venv/bin/python", "-m", "gunicorn", "pycon.wsgi:application"]
  env_vars = [
    { name = "DATABASE_URL", value = local.database_url, secret = true },
    { name = "DEBUG", value = "False", secret = false },
    { name = "SECRET_KEY", value = random_password.secret_key.result, secret = true },
    { name = "MAPBOX_PUBLIC_API_KEY", value = data.azurerm_key_vault_secret.mapbox_public_api_key.value, secret = true },
    { name = "SENTRY_DSN", value = data.azurerm_key_vault_secret.sentry_dsn.value, secret = true },
    { name = "VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN", value = data.azurerm_key_vault_secret.volunteers_push_notifications_ios_arn.value, secret = true },
    { name = "VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN", value = data.azurerm_key_vault_secret.volunteers_push_notifications_android_arn.value, secret = true },
    { name = "ALLOWED_HOSTS", value = "*", secret = false },
    { name = "DJANGO_SETTINGS_MODULE", value = "pycon.settings.prod", secret = false },
    { name = "AWS_MEDIA_BUCKET", value = aws_s3_bucket.backend_media.id },
    { name = "AWS_REGION_NAME", value = aws_s3_bucket.backend_media.region },
    { name = "SPEAKERS_EMAIL_ADDRESS", value = data.azurerm_key_vault_secret.speakers_email_address.value },
    { name = "EMAIL_BACKEND", value = "django_ses.SESBackend", secret = false },
    { name = "PYTHONIT_EMAIL_BACKEND", value = "pythonit_toolkit.emails.backends.ses.SESEmailBackend", secret = false },
    { name = "FRONTEND_URL", value = "https://pycon.it", secret = false },
    { name = "PRETIX_API", value = "https://tickets.pycon.it/api/v1/", secret = false },
    { name = "AWS_S3_CUSTOM_DOMAIN", value = local.cdn_url, secret = false },
    { name = "PRETIX_API_TOKEN", value = module.common_secrets.value.pretix_api_token },
    { name = "PINPOINT_APPLICATION_ID", value = "", secret = false },
    { name = "PASTAPORTO_SECRET", value = module.common_secrets.value.pastaporto_secret, secret = true },
    { name = "FORCE_PYCON_HOST", value = var.is_prod, secret = false },
    { name = "ASSOCIATION_BACKEND_SERVICE", value = local.association_backend_url, secret = false },
    { name = "USERS_SERVICE", value = local.users_backend_url, secret = false },
    { name = "SERVICE_TO_SERVICE_SECRET", value = module.common_secrets.value.service_to_service_secret, secret = true },
    { name = "SQS_QUEUE_URL", value = data.aws_sqs_queue.queue.id, secret = false },
    { name = "MAILCHIMP_SECRET_KEY", value = module.common_secrets.value.mailchimp_secret_key, secret = true },
    { name = "MAILCHIMP_DC", value = module.common_secrets.value.mailchimp_dc, secret = false },
    { name = "MAILCHIMP_LIST_ID", value = module.common_secrets.value.mailchimp_list_id, secret = false },
    { name = "USER_ID_HASH_SALT", value = random_password.userid_hash.result, secret = true },
    { name = "AZURE_STORAGE_ACCOUNT_NAME", value = azurerm_storage_account.storage.name, secret = true },
    { name = "AZURE_STORAGE_ACCOUNT_KEY", value = azurerm_storage_account.storage.primary_access_key, secret = true },
    { name = "PLAIN_API", value = "https://core-api.uk.plain.com/graphql/v1", secret = false },
    { name = "PLAIN_API_TOKEN", value = data.azurerm_key_vault_secret.plain_api_token.value, secret = true },
    { name = "ENVIRONMENT", value = var.workspace, secret = false },
  ]
}
