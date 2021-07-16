module "secrets" {
  source = "../../components/secrets"
  service = "users-backend"
}

module "common_secrets" {
  source = "../../components/secrets"
}
