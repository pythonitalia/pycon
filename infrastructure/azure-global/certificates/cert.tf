resource "tls_private_key" "private_key" {
  algorithm = "RSA"
}

resource "acme_registration" "registration" {
  account_key_pem = tls_private_key.private_key.private_key_pem
  email_address   = "info@pycon.it"
}

data "aws_route53_zone" "python_it" {
  name = "python.it"
}

resource "acme_certificate" "python_it" {
  account_key_pem           = acme_registration.registration.account_key_pem
  common_name               = data.aws_route53_zone.python_it.name
  subject_alternative_names = ["*.${data.aws_route53_zone.python_it.name}"]

  dns_challenge {
    provider = "route53"

    config = {
      AWS_HOSTED_ZONE_ID = data.aws_route53_zone.python_it.zone_id
    }
  }

  depends_on = [acme_registration.registration]
}
