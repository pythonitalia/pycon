locals {
  database_url      = "psql://${data.azurerm_key_vault_secret.db_username.value}:${data.azurerm_key_vault_secret.db_password.value}@${data.azurerm_postgresql_flexible_server.db.fqdn}:5432/cms?sslmode=require"
  users_backend_url = var.is_prod ? "https://users-api.python.it" : "https://pastaporto-users-api.python.it"
}

resource "random_password" "secret_key" {
  length           = 32
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
  env_vars = [
    { name = "DEBUG", value = "true", secret = false },
    { name = "SECRET_KEY", value = random_password.secret_key.result, secret = false },
    { name = "DATABASE_URL", value = local.database_url, secret = true },
    { name = "USERS_SERVICE", value = local.users_backend_url, secret = false },
    { name = "SERVICE_TO_SERVICE_SECRET", value = data.azurerm_key_vault_secret.service_to_service_secret.value, secret = true },
  ]
}
