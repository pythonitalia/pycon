locals {
  cdn_domain = local.is_prod ? "cdn.pycon.it" : "${terraform.workspace}-cdn.pycon.it"
}

resource "aws_cloudfront_distribution" "media_cdn" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "${terraform.workspace} Media CDN"
  wait_for_deployment = false
  aliases             = [local.cdn_domain]

  origin {
    domain_name = aws_s3_bucket.backend_media.bucket_regional_domain_name
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
    acm_certificate_arn            = data.aws_acm_certificate.cert.arn
  }

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "default"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
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

data "aws_route53_zone" "pycon_zone" {
  name = "pycon.it"
}

resource "aws_route53_record" "cdn_record" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = local.cdn_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.media_cdn.domain_name
    zone_id                = aws_cloudfront_distribution.media_cdn.hosted_zone_id
    evaluate_target_health = false
  }
}
