# We do not need to add any route53 route because
# we already have one 1 for the certificate in US-EAST-1
resource "aws_acm_certificate" "eu_central_1_cert" {
  domain_name               = "*.beta.python.it"
  subject_alternative_names = []
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}
