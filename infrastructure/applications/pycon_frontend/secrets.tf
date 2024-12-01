module "secrets" {
  source  = "../../components/secrets"
  service = "pycon-frontend"
}

module "common_secrets" {
  source = "../../components/secrets"
}
