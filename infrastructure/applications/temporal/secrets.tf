module "secrets" {
  source  = "../../components/secrets"
  service = "temporal"
}

module "pycon_be_secrets" {
  source  = "../../components/secrets"
  service = "pycon-backend"
}

module "common_secrets" {
  source = "../../components/secrets"
}
