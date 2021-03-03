resource "aws_acm_certificate" "cert" {
  domain_name               = "*.beta.python.it"
  subject_alternative_names = []
  validation_method         = "DNS"
  provider                  = aws.us

  lifecycle {
    create_before_destroy = true
  }
}

data "aws_route53_zone" "domain" {
  name = "python.it."
}

resource "aws_route53_record" "validation" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  name    = each.value.name
  type    = each.value.type
  zone_id = data.aws_route53_zone.domain.zone_id
  records = [each.value.record]
  ttl     = 60
}
