resource "aws_route53_record" "pycon_it_a" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "pycon.it"
  type    = "A"
  records = ["76.76.21.21"]
  ttl     = "3600"
}

resource "aws_route53_record" "pycon_it_mx" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "pycon.it"
  type    = "MX"
  records = ["5 alt2.aspmx.l.google.com.", "5 alt1.aspmx.l.google.com.", "1 aspmx.l.google.com.", "10 aspmx5.googlemail.com.", "10 aspmx4.googlemail.com.", "10 aspmx3.googlemail.com.", "10 aspmx2.googlemail.com."]
  ttl     = "172800"
}

resource "aws_route53_record" "pycon_it_ns" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "pycon.it"
  type    = "NS"
  records = ["ns-774.awsdns-32.net.", "ns-1337.awsdns-39.org.", "ns-1872.awsdns-42.co.uk.", "ns-314.awsdns-39.com."]
  ttl     = "172800"
}

resource "aws_route53_record" "pycon_it_soa" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "pycon.it"
  type    = "SOA"
  records = ["ns-774.awsdns-32.net. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400"]
  ttl     = "900"
}

resource "aws_route53_record" "pycon_it_txt" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "pycon.it"
  type    = "TXT"
  records = ["google-site-verification=2xGze4V03dEnQJ7YEdXIBrjc98Cck2Kof8GQB1hlQTg", "amazonses:LN511xLUx1n9j6YUh37hEg1t1TtF9TDvjlZzrGnZD5o=", "v=spf1 ip4:2.228.72.10 ip6:2001:b02:400:1::10 ip4:2.228.72.51 ip4:2.228.72.55 ip6:2001:b02:400:1::55 include:amazonses.com include:_spf.google.com a ~all"]
  ttl     = "172800"
}

resource "aws_route53_record" "amazonses_pycon_it_txt" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "_amazonses.pycon.it"
  type    = "TXT"
  records = ["LN511xLUx1n9j6YUh37hEg1t1TtF9TDvjlZzrGnZD5o="]
  ttl     = "3600"
}

resource "aws_route53_record" "assopy_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "assopy.pycon.it"
  type    = "CNAME"
  records = ["pycon.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "beta_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "beta.pycon.it"
  type    = "CNAME"
  records = ["pycon.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "contest_pycon_it_a" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "contest.pycon.it"
  type    = "A"
  records = ["10.128.33.64"]
  ttl     = "3600"
}

resource "aws_route53_record" "ep2011_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "ep2011.pycon.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "ep2012_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "ep2012.pycon.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "ep2013_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "ep2013.pycon.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "hg_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "hg.pycon.it"
  type    = "CNAME"
  records = ["pycon.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "legacy_pycon_it_a" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "legacy.pycon.it"
  type    = "A"
  records = ["2.228.72.51"]
  ttl     = "3600"
}

resource "aws_route53_record" "netlify_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "netlify.pycon.it"
  type    = "CNAME"
  records = ["pycon-italia.netlify.com."]
  ttl     = "3600"
}

resource "aws_route53_record" "pydata_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "pydata.pycon.it"
  type    = "CNAME"
  records = ["host.launchrock.com."]
  ttl     = "3600"
}

resource "aws_route53_record" "pyriddle13_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "pyriddle13.pycon.it"
  type    = "CNAME"
  records = ["pyriddle13.herokuapp.com."]
  ttl     = "3600"
}

resource "aws_route53_record" "riddle_pycon_it_a" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "riddle.pycon.it"
  type    = "A"
  records = ["10.128.33.64"]
  ttl     = "3600"
}

resource "aws_route53_record" "slack_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "slack.pycon.it"
  type    = "CNAME"
  records = ["pycon-nove-slack.herokuapp.com."]
  ttl     = "3600"
}

resource "aws_route53_record" "wasp_pycon_it_a" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "wasp.pycon.it"
  type    = "A"
  records = ["10.128.33.64"]
  ttl     = "3600"
}

resource "aws_route53_record" "wasp10_pycon_it_a" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "wasp10.pycon.it"
  type    = "A"
  records = ["10.128.33.64"]
  ttl     = "3600"
}

resource "aws_route53_record" "wasp10x_pycon_it_a" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "wasp10x.pycon.it"
  type    = "A"
  records = ["10.128.33.64"]
  ttl     = "3600"
}

resource "aws_route53_record" "wiki_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "wiki.pycon.it"
  type    = "CNAME"
  records = ["pycon.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "www_pycon_it_cname" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "www.pycon.it"
  type    = "CNAME"
  records = ["pycon.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "pycon_2022" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "2022.pycon.it"
  type    = "CNAME"
  records = ["2022.pycon.it.s3-website.eu-central-1.amazonaws.com"]
  ttl     = "3600"
}

resource "aws_route53_record" "pycon_2023" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "2023.pycon.it"
  type    = "CNAME"
  records = ["cname.vercel-dns.com"]
  ttl     = "3600"
}

resource "aws_route53_record" "pycon_2024" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "2024.pycon.it"
  type    = "CNAME"
  records = ["cname.vercel-dns.com"]
  ttl     = "3600"
}

resource "aws_route53_record" "pycon_2025" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "2025.pycon.it"
  type    = "CNAME"
  records = ["cname.vercel-dns.com"]
  ttl     = "3600"
}

resource "aws_route53_record" "email_flodesk" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "fde._domainkey.pycon.it"
  type    = "CNAME"
  records = ["dkim.dxjyvt.fg84.fdske.com"]
  ttl     = "3600"
}

resource "aws_route53_record" "email_flodesk_2" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "fdesp.pycon.it"
  type    = "CNAME"
  records = ["spf.dxjyvt.fg84.fdske.com"]
  ttl     = "3600"
}

resource "aws_route53_record" "flodesk_dmarc" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "_dmarc"
  type    = "TXT"
  records = ["v=DMARC1; p=none"]
  ttl     = "900"
}

resource "aws_route53_record" "postmark_dkim" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "20241118190136pm._domainkey"
  type    = "TXT"
  records = ["k=rsa;p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCNrZ0k+aFz4r58EgEAhZhieJgjAxwXiGaAXbaGYeeFyTJqLH+/bqxJ0+mkqnI5PZhXAGBJ7t1ZWmbTtD2Ul//efTOAiQO1inK0yXLwsiYJkuQUYJRbOfcLZd2QYjLK9CE1Gz1cZOzHhJB/Hho5yK/Ul+FeqJVG5qAuLM06Ga4VUwIDAQAB"]
  ttl     = "900"
}

resource "aws_route53_record" "postmark_bounces" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "pm-bounces"
  type    = "CNAME"
  records = ["pm.mtasv.net"]
  ttl     = "900"
}

resource "aws_route53_record" "google_dkim" {
  zone_id = aws_route53_zone.pyconit.id
  name    = "google._domainkey"
  type    = "TXT"
  records = ["v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCItu6XrQBz+OzJ/5S3ToRx94ZHJTTX6VTRuAmlAeGbzcJjh7Y1eBnhCjaSpdzY1asKYrWH2h2iteB778Za/OGTMbgIalEEPywSWbLxKXum59x5uZ8nR77HL658gamU/yx4cQZzv+pr0Cnr+9lgvqckFnJ3X4lllR56Xcqmo4rWAQIDAQAB"]
  ttl     = "900"
}
