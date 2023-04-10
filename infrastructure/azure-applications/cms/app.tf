locals {
  database_url      = "psql://${data.azurerm_key_vault_secret.db_username.value}:${data.azurerm_key_vault_secret.db_password.value}@${data.azurerm_postgresql_flexible_server.db.fqdn}:5432/cms?sslmode=require"
  users_backend_url = var.is_prod ? "https://users-api.python.it" : "https://pastaporto-users-api.python.it"
  domain            = var.is_prod ? "cms.python.it" : "${var.workspace}-cms.python.it"
}

resource "random_password" "secret_key" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "random_password" "revalidate_secret" {
  length           = 128
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

data "azurerm_postgresql_flexible_server" "db" {
  name                = "pythonit-${var.workspace}-database"
  resource_group_name = var.resource_group_name
}

module "app" {
  source              = "../components/container_app"
  service_name        = "cms"
  resource_group_name = var.resource_group_name
  workspace           = var.workspace
  githash             = var.githash
  environment_name    = "pythonit-${var.workspace}-env"
  healthcheck_path    = "/graphql/"
  port                = 8000
  domain              = local.domain
  env_vars = [
    { name = "DEBUG", value = "false", secret = false },
    { name = "ENVIRONMENT", value = var.workspace, secret = false },
    { name = "SENTRY_DSN", value = data.azurerm_key_vault_secret.sentry_dsn.value, secret = true },
    { name = "SECRET_KEY", value = random_password.secret_key.result, secret = true },
    { name = "DATABASE_URL", value = local.database_url, secret = true },
    { name = "USERS_SERVICE", value = local.users_backend_url, secret = false },
    { name = "MAPBOX_PUBLIC_API_KEY", value = data.azurerm_key_vault_secret.mapbox_public_api_key.value, secret = false },
    { name = "SERVICE_TO_SERVICE_SECRET", value = data.azurerm_key_vault_secret.service_to_service_secret.value, secret = true },
    { name = "AZURE_ACCOUNT_NAME", value = azurerm_storage_account.storage.name, secret = false },
    { name = "AZURE_ACCOUNT_KEY", value = azurerm_storage_account.storage.primary_access_key, secret = true },
    { name = "AZURE_CONTAINER", value = azurerm_storage_container.media.name, secret = false },
    { name = "REVALIDATE_SECRET", value = random_password.revalidate_secret.result, secret = true },
  ]
}
