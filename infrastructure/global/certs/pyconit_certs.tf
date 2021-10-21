data "aws_route53_zone" "pyconit_domain" {
  name = "pycon.it."
}

resource "aws_acm_certificate" "pyconit_cert" {
  domain_name               = "*.pycon.it"
  subject_alternative_names = []
  validation_method         = "DNS"
  provider                  = aws.us

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "pyconit_validation" {
  for_each = {
    for dvo in aws_acm_certificate.pyconit_cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  name    = each.value.name
  type    = each.value.type
  zone_id = data.aws_route53_zone.pyconit_domain.zone_id
  records = [each.value.record]
  ttl     = 60
}
