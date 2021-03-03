resource "aws_apigatewayv2_domain_name" "domain" {
  count       = var.use_domain ? 1 : 0
  domain_name = var.domain

  domain_name_configuration {
    certificate_arn = var.certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

resource "aws_apigatewayv2_api_mapping" "domain" {
  count = var.use_domain ? 1 : 0

  api_id      = aws_apigatewayv2_api.api.id
  domain_name = aws_apigatewayv2_domain_name.domain[0].id
  stage       = aws_apigatewayv2_stage.default.id
}

data "aws_route53_zone" "zone" {
  count = var.use_domain ? 1 : 0
  name  = var.zone_name
}

resource "aws_route53_record" "record" {
  count   = var.use_domain ? 1 : 0
  name    = aws_apigatewayv2_domain_name.domain[0].domain_name
  type    = "A"
  zone_id = data.aws_route53_zone.zone[0].zone_id

  alias {
    name                   = aws_apigatewayv2_domain_name.domain[0].domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.domain[0].domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}
