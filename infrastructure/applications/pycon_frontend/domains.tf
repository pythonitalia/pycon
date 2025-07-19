data "aws_route53_zone" "zone" {
  name = "pycon.it"
}

resource "aws_route53_record" "pycon_2026" {
  count = local.is_prod ? 1 : 0
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = "2026.pycon.it"
  type    = "A"

  alias {
    name                   = var.cf_domain_name
    zone_id                = var.cf_hosted_zone_id
    evaluate_target_health = false
  }
}
