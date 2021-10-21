data "aws_route53_zone" "pythonit_domain" {
  name = "python.it."
}

# US Cert
resource "aws_acm_certificate" "pythonit_cert" {
  domain_name               = "*.python.it"
  subject_alternative_names = []
  validation_method         = "DNS"
  provider                  = aws.us

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "pythonit_validation" {
  for_each = {
    for dvo in aws_acm_certificate.pythonit_cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  name    = each.value.name
  type    = each.value.type
  zone_id = data.aws_route53_zone.pythonit_domain.zone_id
  records = [each.value.record]
  ttl     = 60
}


# EU Central 1 Cert
resource "aws_acm_certificate" "pythonit_eu_central_1_cert" {
  domain_name               = "*.python.it"
  subject_alternative_names = []
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}
