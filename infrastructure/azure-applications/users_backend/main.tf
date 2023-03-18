locals {
  database_url = "postgresql+asyncpg://${data.azurerm_key_vault_secret.db_username.value}:${data.azurerm_key_vault_secret.db_password.value}@${data.azurerm_postgresql_flexible_server.db.fqdn}:5432/users"
}

data "azurerm_postgresql_flexible_server" "db" {
  name                = "pythonit-${var.workspace}-database"
  resource_group_name = var.resource_group_name
}

module "ca_app" {
  source              = "../components/container_app"
  service_name        = "users-backend"
  resource_group_name = var.resource_group_name
  workspace           = var.workspace
  githash             = var.githash
  environment_name    = "pythonit-${var.workspace}-env"
  command             = ["/home/app/.venv/bin/python", "-m", "gunicorn", "main:wrapped_app"]
  port = 8000
  env_vars = [
    {
      name  = "DEBUG"
      value = "true", secret = false
    },
    { name = "SECRET_KEY", value = data.azurerm_key_vault_secret.secret_key.value, secret = true },
    { name = "GOOGLE_AUTH_CLIENT_ID", value = "empty", secret = false },
    { name = "GOOGLE_AUTH_CLIENT_SECRET", value = "empty", secret = false },
    { name = "DATABASE_URL", value = local.database_url, secret = true },
    { name = "EMAIL_BACKEND", value = "pythonit_toolkit.emails.backends.ses.SESEmailBackend", secret = false },
    { name = "SENTRY_DSN", value = "https://caf549e5f57d486aa04491dd75f8bcd0@o296856.ingest.sentry.io/5778704", secret = false },

    { name = "PASTAPORTO_SECRET", value = data.azurerm_key_vault_secret.pastaporto_secret.value, secret = true },
    { name = "IDENTITY_SECRET", value = data.azurerm_key_vault_secret.identity_secret.value, secret = true },
    { name = "SERVICE_TO_SERVICE_SECRET", value = data.azurerm_key_vault_secret.service_to_service_secret.value, secret = true },

    { name = "ASSOCIATION_FRONTEND_URL", value = "https://associazione.python.it", secret = false },

    { name = "DB_SSL_MODE", value = "require", secret = false }
  ]
}
