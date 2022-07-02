data "aws_route53_zone" "zone" {
  name = "pycon.it"
}

data "aws_acm_certificate" "cert" {
  domain   = "*.pycon.it"
  statuses = ["ISSUED"]
  provider = aws.us
}


resource "aws_s3_bucket" "archive_2022" {
  bucket = "2022.pycon.it"
  acl    = "public-read"

  website {
    index_document = "index.html"
  }
}

resource "aws_route53_record" "record" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = "2022"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.pycon_it_2022.domain_name
    zone_id                = aws_cloudfront_distribution.pycon_it_2022.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_cloudfront_distribution" "pycon_it_2022" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "pycon italia 2022 archived website"
  wait_for_deployment = false
  aliases             = ["2022.pycon.it"]

  origin {
    domain_name = aws_s3_bucket.archive_2022.website_endpoint
    origin_id   = "website"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1", "TLSv1.1", "TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "website"

    forwarded_values {
      query_string = true

      cookies {
        forward = "none"
      }

      headers = ["Origin"]
    }

    viewer_protocol_policy = "allow-all"
    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = false
    minimum_protocol_version       = "TLSv1"
    ssl_support_method             = "sni-only"
    acm_certificate_arn            = data.aws_acm_certificate.cert.arn
  }
}
