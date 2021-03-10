data "aws_route53_zone" "pyconit" {
  name = "pycon.it"
}

resource "aws_route53_record" "admin" {
  zone_id = data.aws_route53_zone.pyconit.zone_id
  name    = "admin"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.backend_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.backend_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}
