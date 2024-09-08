locals {
  pycon_web_domain = local.is_prod ? "admin.pycon.it" : "${terraform.workspace}-admin.pycon.it"
  pretix_web_domain = local.is_prod ? "tickets.pycon.it" : "${terraform.workspace}-tickets.pycon.it"
}

data "aws_instance" "server" {
  instance_tags = {
    Name = "pythonit-${terraform.workspace}-server"
  }

  filter {
    name   = "instance-state-name"
    values = ["running"]
  }
}

data "aws_cloudfront_origin_request_policy" "all_viewer" {
  name = "Managed-AllViewer"
}

data "aws_cloudfront_cache_policy" "caching_disabled" {
  name = "Managed-CachingDisabled"
}

data "aws_acm_certificate" "cert" {
  domain   = "*.pycon.it"
  statuses = ["ISSUED"]
  provider = aws.us
}

resource "aws_cloudfront_distribution" "application" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "${terraform.workspace} server"
  wait_for_deployment = false
  aliases             = [
    local.pycon_web_domain,
    local.pretix_web_domain
  ]

  origin {
    domain_name = data.aws_instance.server.public_dns
    origin_id   = "default"

    custom_origin_config {
      origin_protocol_policy = "http-only"
      http_port              = "80"
      https_port             = "443"
      origin_ssl_protocols   = ["TLSv1"]
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = false
    minimum_protocol_version       = "TLSv1"
    ssl_support_method             = "sni-only"
    acm_certificate_arn            = data.aws_acm_certificate.cert.arn
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "default"

    cache_policy_id          = data.aws_cloudfront_cache_policy.caching_disabled.id
    origin_request_policy_id = data.aws_cloudfront_origin_request_policy.all_viewer.id

    viewer_protocol_policy = "redirect-to-https"
    compress               = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}
