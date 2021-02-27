locals {
  backend_lambda_function_name = "${terraform.workspace}-pycon-backend"
}

data "aws_db_instance" "database" {
  db_instance_identifier = "terraform-20190815202105324300000001"
}

data "aws_vpc" "default" {
  filter {
    name   = "tag:Name"
    values = ["pythonit-vpc"]
  }
}


data "aws_security_group" "rds" {
  name = "pythonit-rds-security-group"
}

data "aws_security_group" "lambda" {
  name = "pythonit-lambda-security-group"
}

data "aws_subnet_ids" "private" {
  vpc_id = data.aws_vpc.default.id

  tags = {
    Type = "private"
  }
}

resource "aws_lambda_function" "backend_lambda" {
  function_name = local.backend_lambda_function_name
  role          = aws_iam_role.backend_role.arn
  image_uri     = local.backend_image_uri
  package_type  = "Image"
  timeout       = 30
  depends_on    = [aws_iam_role_policy.backend_lambda]
  memory_size   = 512

  vpc_config {
    subnet_ids         = [for subnet in data.aws_subnet_ids.private.ids : subnet]
    security_group_ids = [data.aws_security_group.rds.id, data.aws_security_group.lambda.id]
  }

  environment {
    variables = {
      DATABASE_URL                     = "postgres://${data.aws_db_instance.database.master_username}:${var.database_password}@${data.aws_db_instance.database.address}:${data.aws_db_instance.database.port}/${data.aws_db_instance.database.db_name}"
      DEBUG                            = "False"
      SECRET_KEY                       = var.secret_key
      MAPBOX_PUBLIC_API_KEY            = var.mapbox_public_api_key
      SENTRY_DSN                       = var.sentry_dsn
      SLACK_INCOMING_WEBHOOK_URL       = var.slack_incoming_webhook_url
      ALLOWED_HOSTS                    = "*"
      DJANGO_SETTINGS_MODULE           = "pycon.settings.prod"
      AWS_MEDIA_BUCKET                 = aws_s3_bucket.backend_media.id
      AWS_REGION_NAME                  = aws_s3_bucket.backend_media.region
      EMAIL_BACKEND                    = "django_ses.SESBackend"
      FRONTEND_URL                     = "https://pycon.it"
      PRETIX_API                       = "https://tickets.pycon.it/api/v1/"
      PRETIX_API_TOKEN                 = var.pretix_api_token
      PINPOINT_APPLICATION_ID          = var.pinpoint_application_id
      SOCIAL_AUTH_GOOGLE_OAUTH2_KEY    = var.social_auth_google_oauth2_key
      SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = var.social_auth_google_oauth2_secret
    }
  }
}

resource "aws_iam_role" "backend_role" {
  name = "${terraform.workspace}-pycon-backend-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "backend_lambda" {
  name = "${terraform.workspace}-pycon-backend-role"
  role = aws_iam_role.backend_role.id

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "${aws_cloudwatch_log_group.backend_lambda.arn}:*:*",
        "Effect": "Allow"
      },
      {
        "Action": [
          "ec2:DescribeNetworkInterfaces",
          "ec2:CreateNetworkInterface",
          "ec2:DeleteNetworkInterface",
          "ec2:DescribeInstances",
          "ec2:AttachNetworkInterface",
          "ses:*"
        ],
        "Resource": "*",
        "Effect": "Allow"
      },
      {
        "Action": [
          "s3:*"
        ],
        "Resource": [
          "${aws_s3_bucket.backend_media.arn}",
          "${aws_s3_bucket.backend_media.arn}/*"
        ],
        "Effect": "Allow"
      }
    ]
  }
  EOF
}

resource "aws_lambda_permission" "backend_apigw" {
  statement_id  = "${terraform.workspace}-allow-apigateway-invoke"
  action        = "lambda:InvokeFunction"
  function_name = local.backend_lambda_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}

resource "aws_cloudwatch_log_group" "backend_lambda" {
  name              = "/aws/lambda/${local.backend_lambda_function_name}"
  retention_in_days = 7
}
