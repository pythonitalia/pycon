module "secrets" {
  source  = "../../components/secrets"
  service = "gateway"
}

module "common_secrets" {
  source = "../../components/secrets"
}
