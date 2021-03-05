locals {
  is_prod = terraform.workspace == "production"
  domain  = local.is_prod ? "${local.domain_name}.beta.python.it" : "${terraform.workspace}-${local.domain_name}.beta.python.it"

  # Services URLs
  users_service_url = local.is_prod ? "https://users-api.beta.python.it" : "https://${terraform.workspace}-users-api.beta.python.it"
}

data "aws_iam_role" "lambda" {
  name = "pythonit-lambda-role"
}

module "lambda" {
  source = "../../components/application_lambda"

  application = local.application
  docker_tag  = "production"
  role_arn    = data.aws_iam_role.lambda.arn
  env_vars = {
    NODE_ENV      = "production"
    VARIANT       = "default"
    USERS_SERVICE = local.users_service_url

    # Secrets
    PASTAPORTO_SECRET         = var.pastaporto_secret
    IDENTITY_SECRET           = var.identity_secret
    SERVICE_TO_SERVICE_SECRET = var.service_to_service_secret
  }
}

module "api" {
  source = "../../components/http_api_gateway"

  application          = local.application
  lambda_invoke_arn    = module.lambda.invoke_arn
  lambda_function_name = module.lambda.function_name
}

data "aws_acm_certificate" "beta" {
  domain   = "*.beta.python.it"
  statuses = ["ISSUED"]
  provider = aws.us
}

module "distribution" {
  source = "../../components/cloudfront"

  application     = local.application
  zone_name       = "python.it"
  domain          = local.domain
  certificate_arn = data.aws_acm_certificate.beta.arn
  origin_url      = module.api.cloudfront_friendly_endpoint
}
