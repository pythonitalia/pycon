data "aws_cloudfront_cache_policy" "caching_disabled" {
  name = "Managed-CachingDisabled"
}

data "aws_cloudfront_origin_request_policy" "all_viewer" {
  name = "Managed-AllViewer"
}

resource "aws_acm_certificate" "cert" {
  domain_name       = local.email_tracking_domain
  validation_method = "DNS"
  provider = aws.us
}

data "aws_route53_zone" "pythonit" {
  name = "python.it"
}

resource "aws_route53_record" "email_tracking" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.pythonit.zone_id
}

resource "aws_cloudfront_distribution" "email_tracking" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "${terraform.workspace} Email tracking"
  wait_for_deployment = false
  aliases             = [local.email_tracking_domain]

  origin {
    domain_name = "r.eu-central-1.awstrack.me"
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
    acm_certificate_arn            = aws_acm_certificate.cert.arn
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "default"

    cache_policy_id = data.aws_cloudfront_cache_policy.caching_disabled.id
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

resource "aws_route53_record" "record" {
  zone_id = data.aws_route53_zone.pythonit.zone_id
  name    = local.email_tracking_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.email_tracking.domain_name
    zone_id                = aws_cloudfront_distribution.email_tracking.hosted_zone_id
    evaluate_target_health = false
  }
}
