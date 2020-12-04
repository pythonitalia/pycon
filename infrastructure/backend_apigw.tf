locals {
  api_endpoint = replace(aws_apigatewayv2_api.backend.api_endpoint, "/^https?://([^/]*).*/", "$1")
}

resource "aws_apigatewayv2_api" "backend" {
  name          = "${terraform.workspace}-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "backend_lambda" {
  api_id               = aws_apigatewayv2_api.backend.id
  integration_type     = "AWS_PROXY"
  connection_type      = "INTERNET"
  description          = "Lambda"
  integration_method   = "POST"
  integration_uri      = aws_lambda_function.backend_lambda.invoke_arn
  passthrough_behavior = "WHEN_NO_MATCH"
}

resource "aws_apigatewayv2_stage" "backend_default" {
  api_id        = aws_apigatewayv2_api.backend.id
  name          = "$default"
  deployment_id = aws_apigatewayv2_deployment.backend.id

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.backend_lambda.arn
    format          = "$context.identity.sourceIp - - [$context.requestTime] \"$context.httpMethod $context.routeKey $context.protocol\" $context.status $context.responseLength $context.requestId $context.integrationErrorMessage"
  }
}

resource "aws_apigatewayv2_deployment" "backend" {
  api_id      = aws_apigatewayv2_api.backend.id
  description = "Deployment"

  triggers = {
    redeployment = sha1(join(",", list(
      jsonencode(aws_apigatewayv2_integration.backend_lambda),
      jsonencode(aws_apigatewayv2_route.backend_default),
      jsonencode(aws_lambda_permission.backend_apigw),
    )))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_apigatewayv2_route" "backend_default" {
  api_id    = aws_apigatewayv2_api.backend.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.backend_lambda.id}"
}
