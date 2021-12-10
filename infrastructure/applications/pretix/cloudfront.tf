locals {
  is_prod = terraform.workspace == "production"
  alias   = local.is_prod ? "tickets.pycon.it" : "${terraform.workspace}-tickets.pycon.it"
}

resource "aws_cloudfront_distribution" "distribution" {
  aliases = [local.alias]

  origin {
    domain_name = aws_eip.ip.public_dns
    origin_id   = "pretix"

    custom_origin_config {
      origin_protocol_policy = "http-only"
      http_port              = "80"
      https_port             = "443"
      origin_ssl_protocols   = ["TLSv1"]
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Pretix ${terraform.workspace}"
  wait_for_deployment = false

  viewer_certificate {
    cloudfront_default_certificate = false
    acm_certificate_arn            = module.common_secrets.value.ssl_certificate_arn
    minimum_protocol_version       = "TLSv1"
    ssl_support_method             = "sni-only"
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "pretix"

    forwarded_values {
      query_string = true
      headers      = ["*"]

      cookies {
        forward = "all"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    min_ttl                = 0
    default_ttl            = 604800
    max_ttl                = 31536000
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}
