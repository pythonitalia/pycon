data "aws_iam_policy_document" "github_runner_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "github_runner_iam" {
  name               = "github_runner_iam"
  assume_role_policy = data.aws_iam_policy_document.github_runner_assume_role.json
}

resource "aws_iam_role_policy" "github_runner_lambda_policy" {
  name = "github_runner_lambda_policy"
  role = aws_iam_role.github_runner_iam.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

data "archive_file" "github_runner_webhook_artifact" {
  type        = "zip"
  source_file = "${path.root}/lambdas/github_runner_webhook.py"
  output_path = "${path.root}/.archive_files/github_runner_webhook.zip"
}

resource "aws_lambda_function" "github_runner_webhook" {
  function_name = "github_runner_webhook"
  role          = aws_iam_role.github_runner_iam.arn
  handler       = "github_runner_webhook.handler"
  runtime = "python3.13"
  filename         = data.archive_file.github_runner_webhook_artifact.output_path
  source_code_hash = data.archive_file.github_runner_webhook_artifact.output_base64sha256
  environment {
    variables = {
      WEBHOOK_SECRET = random_password.webhook_secret.result
    }
  }
}

resource "aws_lambda_function_url" "github_runner_webhook" {
  function_name      = aws_lambda_function.github_runner_webhook.function_name
  authorization_type = "NONE"
}
