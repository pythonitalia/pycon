module "database" {
  source = "./database"

  database_password = var.database_password
}
