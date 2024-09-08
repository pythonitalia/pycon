data "aws_route53_zone" "pyconit" {
  name = "pycon.it"
}

resource "aws_route53_record" "pycon_web" {
  zone_id = data.aws_route53_zone.pyconit.zone_id
  name    = local.pycon_web_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.application.domain_name
    zone_id                = aws_cloudfront_distribution.application.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "pretix_web" {
  zone_id = data.aws_route53_zone.pyconit.zone_id
  name    = local.pretix_web_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.application.domain_name
    zone_id                = aws_cloudfront_distribution.application.hosted_zone_id
    evaluate_target_health = false
  }
}
