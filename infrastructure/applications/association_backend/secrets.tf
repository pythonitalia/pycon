module "secrets" {
  source  = "../../components/secrets"
  service = "association-backend"
}

module "common_secrets" {
  source = "../../components/secrets"
}
