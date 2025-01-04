locals {
  is_prod           = terraform.workspace == "production"
  admin_domain      = "admin"
  full_admin_domain = local.is_prod ? "${local.admin_domain}.pycon.it" : "${terraform.workspace}-${local.admin_domain}.pycon.it"
  db_connection     = "postgres://${var.database_settings.username}:${var.database_settings.password}@${var.database_settings.address}:${var.database_settings.port}/pycon"
  cdn_url           = local.is_prod ? "cdn.pycon.it" : "${terraform.workspace}-cdn.pycon.it"
}

data "aws_acm_certificate" "cert" {
  domain   = "pycon.it"
  statuses = ["ISSUED"]
  provider = aws.us
}
