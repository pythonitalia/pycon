module "secrets" {
  source  = "../../components/secrets"
  service = "pycon-backend"
}

module "common_secrets" {
  source = "../../components/secrets"
}
