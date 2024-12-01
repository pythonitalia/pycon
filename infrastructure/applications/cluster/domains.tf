data "aws_route53_zone" "zone" {
  name = "pycon.it"
}

resource "aws_route53_record" "web_pycon" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = local.pycon_admin_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.application.domain_name
    zone_id                = aws_cloudfront_distribution.application.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "web_frontend" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = local.pycon_frontend_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.application.domain_name
    zone_id                = aws_cloudfront_distribution.application.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "web_tickets" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = local.pretix_web_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.application.domain_name
    zone_id                = aws_cloudfront_distribution.application.hosted_zone_id
    evaluate_target_health = false
  }
}
