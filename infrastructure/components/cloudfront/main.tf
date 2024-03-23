resource "aws_cloudfront_distribution" "application" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "${terraform.workspace}-${var.application}"
  wait_for_deployment = false
  aliases             = [var.domain]

  origin {
    domain_name = var.origin_url
    origin_id   = "default"

    custom_origin_config {
      origin_protocol_policy = "https-only"
      http_port              = "80"
      https_port             = "443"
      origin_ssl_protocols   = ["TLSv1"]
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = false
    minimum_protocol_version       = "TLSv1"
    ssl_support_method             = "sni-only"
    acm_certificate_arn            = var.certificate_arn
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "default"

    forwarded_values {
      query_string = true
      headers = [
        "Access-Control-Request-Headers",
        "Access-Control-Request-Method",
        "Origin",
        "Authorization",
        "Referer",
        "Accept",
        "Accept-Language"
      ]

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
