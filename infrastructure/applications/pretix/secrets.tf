module "secrets" {
  source = "../../components/secrets"
  service = "pretix"
}

module "common_secrets" {
  source = "../../components/secrets"
}
