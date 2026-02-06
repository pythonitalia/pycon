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
  records = ["v=DKIM1;k=rsa;p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr/vX4g9YEgRabzeWScaBvX4idgMMoTqtlUpRYnbgvoKOY198qYuXR0xtB1JcuVO8Q++9pzVDI2IJS1sFm0uK9uFtWbRLuu2PpyI3sADrJAYtryoyawe2GQgC83yn2aKtAYTdQXp2ZVEEn3TsmcsXPHQ8F+BZP36/5VX2N9VPpaJ0aNVlL9Osk6TXretidOgjrzrcnd+gIp0KU+oEodArZuvimngfk5/5b9m5Nhpg4kRvbZzznjWkGv+UAXjnkgclIt35h5LWkZK/s47V7nIBlAewEEdk93diC5C6JJnxaA9qEGof6RNbj5Qob/r1tZwhVcWHT8O64SzUaH6dsjBsIQIDAQAB"]
  ttl     = "60"
}

resource "aws_route53_record" "pydata_it_mx" {
  zone_id = aws_route53_zone.pydata_it.id
  name    = "pydata.it"
  type    = "MX"
  records = ["1 smtp.google.com."]
  ttl     = "60"
}
