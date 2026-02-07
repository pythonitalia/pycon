resource "aws_route53_record" "pydata_it_txt" {
  zone_id = aws_route53_zone.pydata_it.id
  name    = "pydata.it"
  type    = "TXT"
  records = ["google-site-verification=Lwmb3AJYmMsxy-guo-bUbV3j-Be1a0nbp9c2f4lPmSM"]
  ttl     = "60"
}

resource "aws_route53_record" "pydata_it_dkim" {
  zone_id = aws_route53_zone.pydata_it.id
  name    = "google._domainkey.pydata.it"
  type    = "TXT"
  records = ["v=DKIM1;k=rsa;p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCjEv46PX4U/7HSrVmAvoPWP+ShH3qIjqDeTWZoX132QulLy3YNLjWFIrOPItRs4k13JvRor5GFtfq+xwXil7MXVVQ/6r4mB4WeJX29kCitlXrxm7m25r4Kh4Pomlk0/8VWvB/E8b1aT1l9p8h2VS+boOec0zC9DrqEGpfWQff3awIDAQAB"]
  ttl     = "60"
}

resource "aws_route53_record" "pydata_it_mx" {
  zone_id = aws_route53_zone.pydata_it.id
  name    = "pydata.it"
  type    = "MX"
  records = ["1 smtp.google.com."]
  ttl     = "60"
}
