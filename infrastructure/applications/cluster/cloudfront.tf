locals {
  pycon_admin_domain  = local.is_prod ? "admin.pycon.it" : "${terraform.workspace}-admin.pycon.it"
  pycon_frontend_domain  = local.is_prod ? "frontend.pycon.it" : "${terraform.workspace}-frontend.pycon.it"
  pretix_web_domain = local.is_prod ? "tickets.pycon.it" : "${terraform.workspace}-tickets.pycon.it"
}

data "aws_cloudfront_origin_request_policy" "all_viewer" {
  name = "Managed-AllViewer"
}

data "aws_cloudfront_cache_policy" "caching_disabled" {
  name = "Managed-CachingDisabled"
}

data "aws_cloudfront_cache_policy" "origin_cache_control_headers" {
  name = "UseOriginCacheControlHeaders"
}

data "aws_acm_certificate" "cert" {
  domain   = "pycon.it"
  statuses = ["ISSUED"]
  provider = aws.us
}

resource "aws_cloudfront_distribution" "application" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "${terraform.workspace} server"
  wait_for_deployment = false
  aliases = local.is_prod ? ["*.pycon.it", "pycon.it"] : [
    local.pycon_admin_domain,
    local.pycon_frontend_domain,
    local.pretix_web_domain
  ]

  origin {
    domain_name = aws_eip.server.public_dns
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

  ordered_cache_behavior {
    path_pattern     = "/_next/static/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "default"

    cache_policy_id          = data.aws_cloudfront_cache_policy.origin_cache_control_headers.id
    origin_request_policy_id = data.aws_cloudfront_origin_request_policy.all_viewer.id

    compress               = true
    viewer_protocol_policy = "redirect-to-https"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

output "cf_domain_name" {
  value = aws_cloudfront_distribution.application.domain_name
}

output "cf_hosted_zone_id" {
  value = aws_cloudfront_distribution.application.hosted_zone_id
}
