resource "aws_sesv2_email_identity" "pythonit" {
  email_identity = "python.it"
}

data "aws_route53_zone" "pythonit" {
  name    = "python.it"
}

resource "aws_route53_record" "pythonit_dkim" {
  count = 3

  zone_id = data.aws_route53_zone.pythonit.zone_id
  name    = "${aws_sesv2_email_identity.pythonit.dkim_signing_attributes[0].tokens[count.index]}._domainkey"
  type    = "CNAME"
  ttl     = "600"
  records = ["${aws_sesv2_email_identity.pythonit.dkim_signing_attributes[0].tokens[count.index]}.dkim.amazonses.com"]
  depends_on = [aws_sesv2_email_identity.pythonit]
}
