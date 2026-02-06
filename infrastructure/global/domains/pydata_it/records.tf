resource "aws_route53_record" "pydata_it_txt" {
  zone_id = aws_route53_zone.pydata_it.id
  name    = "pydata.it"
  type    = "TXT"
  records = ["google-site-verification=Lwmb3AJYmMsxy-guo-bUbV3j-Be1a0nbp9c2f4lPmSM"]
  ttl     = "60"
}
