resource "aws_route53_record" "python_it_a" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "python.it"
  type    = "A"
  records = ["2.228.72.55"]
  ttl     = "3600"
}

resource "aws_route53_record" "python_it_mx" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "python.it"
  type    = "MX"
  records = ["10 mail0.develer.com.", "60 mail3.develer.com.", "50 mail2.bertos.org.", "20 mail.python.it.", "70 mail.protonmail.ch", "80 mailsec.protonmail.ch"]
  ttl     = "172800"
}

resource "aws_route53_record" "python_it_ns" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "python.it"
  type    = "NS"
  records = ["ns-70.awsdns-08.com.", "ns-1827.awsdns-36.co.uk.", "ns-1522.awsdns-62.org.", "ns-788.awsdns-34.net."]
  ttl     = "172800"
}

resource "aws_route53_record" "python_it_soa" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "python.it"
  type    = "SOA"
  records = ["ns-70.awsdns-08.com. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400"]
  ttl     = "900"
}

resource "aws_route53_record" "python_it_spf" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "python.it"
  type    = "SPF"
  records = ["v=spf1 include:pycon.it include:_spf.protonmail.ch mx ~all"]
  ttl     = "3600"
}

resource "aws_route53_record" "python_it_txt" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "python.it"
  type    = "TXT"
  records = ["v=spf1 include:pycon.it include:_spf.protonmail.ch mx ~all", "google-site-verification=iuDKJUkUK41L-cG5bU3IcNrBeCmnvV1BlCX2m4W5LJY", "protonmail-verification=aa66b78b1ea723283e5525cdb1000567c801c72b"]
  ttl     = "172800"
}

resource "aws_route53_record" "_dmarc" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "_dmarc"
  type    = "TXT"
  records = ["v=DMARC1; p=none"]
  ttl     = "172800"
}

resource "aws_route53_record" "protonmail_dkim" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "protonmail._domainkey"
  type    = "CNAME"
  records = ["protonmail.domainkey.d7lcpn4eod4w6f4h2xu7f4fi52dbkgmbkavzr23vendi2w23tmemq.domains.proton.ch."]
  ttl     = "3600"
}

resource "aws_route53_record" "protonmail2_dkim" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "protonmail2._domainkey"
  type    = "CNAME"
  records = ["protonmail2.domainkey.d7lcpn4eod4w6f4h2xu7f4fi52dbkgmbkavzr23vendi2w23tmemq.domains.proton.ch."]
  ttl     = "3600"
}

resource "aws_route53_record" "protonmail3_dkim" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "protonmail3._domainkey"
  type    = "CNAME"
  records = ["protonmail3.domainkey.d7lcpn4eod4w6f4h2xu7f4fi52dbkgmbkavzr23vendi2w23tmemq.domains.proton.ch."]
  ttl     = "3600"
}

resource "aws_route53_record" "_matrix__tcp_python_it_srv" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "_matrix._tcp.python.it"
  type    = "SRV"
  records = ["10 0 8448 synapse.python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "associazione_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "associazione"
  type    = "CNAME"
  records = ["cname.vercel-dns.com."]
  ttl     = "3600"
}

resource "aws_route53_record" "beta_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "beta.python.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "docs_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "docs.python.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "hg_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "hg.python.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "lists_python_it_a" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "lists.python.it"
  type    = "A"
  records = ["2.228.72.55"]
  ttl     = "3600"
}

resource "aws_route53_record" "lists_python_it_mx" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "lists.python.it"
  type    = "MX"
  records = ["60 mail3.develer.com.", "50 mail2.bertos.org.", "20 mail.python.it.", "10 mail0.develer.com.", "80 mail5.develer.com."]
  ttl     = "172800"
}

resource "aws_route53_record" "lists_python_it_spf" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "lists.python.it"
  type    = "SPF"
  records = ["v=spf1 include:pycon.it ~all"]
  ttl     = "3600"
}

resource "aws_route53_record" "lists_python_it_txt" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "lists.python.it"
  type    = "TXT"
  records = ["v=spf1 include:pycon.it ~all"]
  ttl     = "3600"
}

resource "aws_route53_record" "mail_python_it_a" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "mail.python.it"
  type    = "A"
  records = ["2.228.72.55"]
  ttl     = "3600"
}

resource "aws_route53_record" "mail_python_it_spf" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "mail.python.it"
  type    = "SPF"
  records = ["v=spf1 include:pycon.it ~all"]
  ttl     = "172800"
}

resource "aws_route53_record" "mail_python_it_txt" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "mail.python.it"
  type    = "TXT"
  records = ["v=spf1 include:pycon.it ~all"]
  ttl     = "172800"
}

resource "aws_route53_record" "milano_python_it_a" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "milano.python.it"
  type    = "CNAME"
  records = ["pythonmilano.github.io"]
  ttl     = "3600"
}

resource "aws_route53_record" "pescara_python_it_a" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "pescara.python.it"
  type    = "CNAME"
  records = ["pythonpescara.github.io"]
  ttl     = "3600"
}

resource "aws_route53_record" "roma_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "roma.python.it"
  type    = "CNAME"
  records = ["pyroma.netlify.com."]
  ttl     = "3600"
}

resource "aws_route53_record" "pydataroma_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "pydataroma.python.it"
  type    = "CNAME"
  records = ["pydataromacapitale.github.io"]
  ttl     = "3600"
}

resource "aws_route53_record" "testcommunity_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "testcommunity.python.it"
  type    = "CNAME"
  records = ["cname.vercel-dns.com."]
  ttl     = "3600"
}

resource "aws_route53_record" "anothercommunity_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "anothercommunity.python.it"
  type    = "CNAME"
  records = ["cname.vercel-dns.com."]
  ttl     = "3600"
}

resource "aws_route53_record" "firenze_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "firenze.python.it"
  type    = "CNAME"
  records = ["cname.vercel-dns.com."]
  ttl     = "3600"
}


resource "aws_route53_record" "bari_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "bari.python.it"
  type    = "CNAME"
  records = ["cname.vercel-dns.com."]
  ttl     = "3600"
}

resource "aws_route53_record" "marche_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "marche.python.it"
  type    = "CNAME"
  records = ["cname.vercel-dns.com."]
  ttl     = "3600"
}

resource "aws_route53_record" "torino_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "torino.python.it"
  type    = "CNAME"
  records = ["cname.vercel-dns.com."]
  ttl     = "3600"
}


resource "aws_route53_record" "varese_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "varese.python.it"
  type    = "CNAME"
  records = ["cname.vercel-dns.com."]
  ttl     = "3600"
}


resource "aws_route53_record" "smtp_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "smtp.python.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "svn_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "svn.python.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "synapse_python_it_a" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "synapse.python.it"
  type    = "A"
  records = ["88.198.151.119"]
  ttl     = "3600"
}

resource "aws_route53_record" "teens_python_it_a" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "teens.python.it"
  type    = "A"
  records = ["51.15.222.47"]
  ttl     = "3600"
}

resource "aws_route53_record" "trac_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "trac.python.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "trento_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "trento.python.it"
  type    = "CNAME"
  records = ["pythonitalia.github.io."]
  ttl     = "3600"
}

resource "aws_route53_record" "catania_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "catania.python.it"
  type    = "CNAME"
  records = ["pythoncatania.github.io."]
  ttl     = "3600"
}

resource "aws_route53_record" "campania_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "campania.python.it"
  type    = "CNAME"
  records = ["pycampania.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "wiki_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "wiki.python.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "www_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "www.python.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "www2_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "www2.python.it"
  type    = "CNAME"
  records = ["python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "socialcards" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "socialcards"
  type    = "CNAME"
  records = ["cname.vercel-dns.com"]
  ttl     = "3600"
}

# social.python.it
# mailgun

resource "aws_route53_record" "mailgun_social_txt" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "social.python.it"
  type    = "TXT"
  records = ["v=spf1 include:mailgun.org ~all"]
  ttl     = "3600"
}

resource "aws_route53_record" "mailgun_social_mta_txt" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "mta._domainkey.social.python.it"
  type    = "TXT"
  records = ["k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDPMH32TC7vXwGqHf42aDvar8rM0+iLYYJSnj3U+ugwzXCCdhrcnaydwpayJ/nI1uVZNPKGIZPIdIoSKVAsbu9lGFv7X/JeTTdik1H7ZnAJ4GZpYl5ogPvMy6vXD7h4UHKsxpmkppmKm3LadcCyu3UUrwrDKaK/KFLNVuLTKWPc9wIDAQAB"]
  ttl     = "3600"
}

resource "aws_route53_record" "social_python_it_mx" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "social.python.it"
  type    = "MX"
  records = ["10 mxa.eu.mailgun.org", "10 mxb.eu.mailgun.org"]
  ttl     = "172800"
}

resource "aws_route53_record" "email_social_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "email.social.python.it"
  type    = "CNAME"
  records = ["eu.mailgun.org"]
  ttl     = "3600"
}

# fly.io

resource "aws_route53_record" "social_python_it_fly" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "social.python.it"
  type    = "A"
  records = ["149.248.213.46"]
  ttl     = "3600"
}

resource "aws_route53_record" "social_python_it_fly_challange" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "_acme-challenge.social.python.it"
  type    = "CNAME"
  records = ["social.python.it.y3xewx.flydns.net."]
  ttl     = "3600"
}

# Fourth Wall Shop

resource "aws_route53_record" "store_python_it_a" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "store.python.it"
  type    = "A"
  records = ["34.117.223.165"]
  ttl     = "3600"
}

resource "aws_route53_record" "www_store_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "www.store"
  type    = "CNAME"
  records = ["store.python.it."]
  ttl     = "3600"
}

resource "aws_route53_record" "em_fw_support_store_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "em-fw.support.store"
  type    = "CNAME"
  records = ["u32554359.wl110.sendgrid.net."]
  ttl     = "3600"
}

resource "aws_route53_record" "s1_domainkey_support_store_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "s1._domainkey.support.store"
  type    = "CNAME"
  records = ["s1.domainkey.u32554359.wl110.sendgrid.net."]
  ttl     = "3600"
}

resource "aws_route53_record" "s2_domainkey_support_store_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "s2._domainkey.support.store"
  type    = "CNAME"
  records = ["s2.domainkey.u32554359.wl110.sendgrid.net."]
  ttl     = "3600"
}

resource "aws_route53_record" "zendesk1_domainkey_support_store_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "zendesk1._domainkey.support.store"
  type    = "CNAME"
  records = ["zendesk1._domainkey.zendesk.com."]
  ttl     = "3600"
}

resource "aws_route53_record" "zendesk2_domainkey_support_store_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "zendesk2._domainkey.support.store"
  type    = "CNAME"
  records = ["zendesk2._domainkey.zendesk.com."]
  ttl     = "3600"
}


resource "aws_route53_record" "zendesk1_support_store_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "zendesk1.support.store"
  type    = "CNAME"
  records = ["mail1.zendesk.com."]
  ttl     = "3600"
}


resource "aws_route53_record" "zendesk2_support_store_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "zendesk2.support.store"
  type    = "CNAME"
  records = ["mail2.zendesk.com."]
  ttl     = "3600"
}


resource "aws_route53_record" "zendesk3_support_store_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "zendesk3.support.store"
  type    = "CNAME"
  records = ["mail3.zendesk.com."]
  ttl     = "3600"
}


resource "aws_route53_record" "zendesk4_support_store_python_it_cname" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "zendesk4.support.store"
  type    = "CNAME"
  records = ["mail4.zendesk.com."]
  ttl     = "3600"
}


resource "aws_route53_record" "zendeskverification_support_store_python_it_txt" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "zendeskverification.support.store"
  type    = "TXT"
  records = ["44c8d8249e7a0c99"]
  ttl     = "3600"
}


resource "aws_route53_record" "_dmarc_support_store_python_it_txt" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "_dmarc.support.store"
  type    = "TXT"
  records = ["v=DMARC1; p=reject; pct=100; rua=mailto:dmarc@fourthwall.com"]
  ttl     = "3600"
}


resource "aws_route53_record" "support_store_python_it_txt" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "support.store"
  type    = "TXT"
  records = ["v=spf1 include:_spf.google.com include:mail.zendesk.com include:spf.improvmx.com include:sendgrid.net ~all"]
  ttl     = "3600"
}


resource "aws_route53_record" "support_store_python_it_mx" {
  zone_id = aws_route53_zone.pythonit.id
  name    = "support.store"
  type    = "MX"
  records = ["10 mx1.improvmx.com.", "20 mx2.improvmx.com."]
  ttl     = "3600"
}
