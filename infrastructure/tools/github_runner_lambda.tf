data "aws_iam_policy_document" "github_runner_webhook_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "github_runner_webhook_role" {
  name               = "github_runner_webhook_role"
  assume_role_policy = data.aws_iam_policy_document.github_runner_webhook_assume_role.json
}

data "aws_ssm_parameter" "github_token" {
  name = "/github-runner/github-token"
}

resource "aws_iam_role_policy" "github_runner_webhook_lambda_policy" {
  name = "github_runner_webhook_lambda_policy"
  role = aws_iam_role.github_runner_webhook_role.id

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
      },
      {
        Effect   = "Allow"
        Action   = [
          "ssm:GetParameter"
        ]
        Resource = [
          data.aws_ssm_parameter.github_token.arn
        ]
      },
      {
        Effect   = "Allow"
        Action   = [
          "ecs:RunTask"
        ]
        Resource = [
          "${aws_ecs_task_definition.github_runner.arn}*",
        ]
      },
      {
        Effect   = "Allow"
        Action   = [
          "iam:PassRole"
        ]
        Resource = [
          aws_iam_role.github_runner_execution_role.arn
        ]
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
  role          = aws_iam_role.github_runner_webhook_role.arn
  handler       = "github_runner_webhook.handler"
  runtime = "python3.13"
  filename         = data.archive_file.github_runner_webhook_artifact.output_path
  source_code_hash = data.archive_file.github_runner_webhook_artifact.output_base64sha256
  timeout = 60

  environment {
    variables = {
      WEBHOOK_SECRET = random_password.webhook_secret.result
      GITHUB_TOKEN_SSM_NAME = data.aws_ssm_parameter.github_token.name
      NETWORK_CONFIGURATION = jsonencode({
        "awsvpcConfiguration": {
          "subnets": [aws_subnet.public["eu-central-1a"].id],
          "securityGroups": [],
          "assignPublicIp": "ENABLED"
        }
      })
      ECS_CLUSTER_NAME = aws_ecs_cluster.github_runners.name
      ECS_TASK_DEFINITION = aws_ecs_task_definition.github_runner.arn
    }
  }
}

resource "aws_lambda_function_url" "github_runner_webhook" {
  function_name      = aws_lambda_function.github_runner_webhook.function_name
  authorization_type = "NONE"
}
