data "aws_route53_zone" "zone" {
  name = "python.it"
}

resource "aws_route53_record" "record" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = "admin"
  type    = "A"
  ttl     = 60
  records = [aws_eip.ip.public_ip]
}
