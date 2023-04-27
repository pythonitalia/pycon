locals {
  database_url             = "postgresql+asyncpg://${data.azurerm_key_vault_secret.db_username.value}:${data.azurerm_key_vault_secret.db_password.value}@${data.azurerm_postgresql_flexible_server.db.fqdn}:5432/users?ssl=require"
  domain                   = var.is_prod ? "azure-users-api.python.it" : "${var.workspace}-users-api.python.it"
  association_frontend_url = "https://associazione.python.it"
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

module "app" {
  source                = "../components/container_app"
  service_name          = "users-backend"
  service_resource_name = "users"
  resource_group_name   = var.resource_group_name
  workspace             = var.workspace
  githash               = var.githash
  environment_name      = "pythonit-${var.workspace}-env"
  healthcheck_path      = "/graphql"
  port                  = 8000
  domain                = local.domain
  command               = ["/home/app/.venv/bin/python", "-m", "gunicorn", "main:wrapped_app"]
  env_vars = [
    { name = "DEBUG", value = "false", secret = false },
    { name = "ENVIRONMENT", value = var.workspace, secret = false },
    { name = "SECRET_KEY", value = random_password.secret_key.result, secret = true },
    { name = "DATABASE_URL", value = local.database_url, secret = true },
    { name = "SENTRY_DSN", value = data.azurerm_key_vault_secret.sentry_dsn.value, secret = true },
    { name = "GOOGLE_AUTH_CLIENT_ID", value = "", secret = false },
    { name = "GOOGLE_AUTH_CLIENT_ID", value = "", secret = false },
    { name = "EMAIL_BACKEND", value = "pythonit_toolkit.emails.backends.ses.SESEmailBackend", secret = false },
    { name = "ASSOCIATION_FRONTEND_URL", value = local.association_frontend_url, secret = false },
    { name = "PASTAPORTO_SECRET", value = data.azurerm_key_vault_secret.pastaporto_secret.value, secret = true },
    { name = "IDENTITY_SECRET", value = data.azurerm_key_vault_secret.pastaporto_secret.value, secret = true },
    { name = "SERVICE_TO_SERVICE_SECRET", value = data.azurerm_key_vault_secret.service_to_service_secret.value, secret = true },
  ]
}
