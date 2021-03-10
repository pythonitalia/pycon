locals {
  lambda_name = "${terraform.workspace}-${var.application}"
  base_env_vars = {
    ENV = terraform.workspace
  }
  env_vars = merge(var.env_vars, local.base_env_vars)
  use_vpc  = length(var.security_group_ids) != 0 && length(var.subnet_ids) != 0
}

resource "aws_lambda_function" "lambda" {
  function_name = local.lambda_name
  role          = var.role_arn
  timeout       = 30
  memory_size   = 512
  package_type  = "Image"
  image_uri     = local.image_uri

  dynamic "vpc_config" {
    for_each = local.use_vpc ? [1] : []

    content {
      subnet_ids         = var.subnet_ids
      security_group_ids = var.security_group_ids
    }
  }

  environment {
    variables = local.env_vars
  }

  tags = {
    Name = var.application
    Env  = terraform.workspace
  }
}

resource "aws_cloudwatch_log_group" "logs" {
  name              = "/aws/lambda/${local.lambda_name}"
  retention_in_days = 7
}

output "invoke_arn" {
  value = aws_lambda_function.lambda.invoke_arn
}

output "function_name" {
  value = local.lambda_name
}
