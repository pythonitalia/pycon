data "aws_iam_policy_document" "github_runner_execution_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ecs.amazonaws.com", "ecs-tasks.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "github_runner_execution_role" {
  name               = "github_runner_execution_role"
  assume_role_policy = data.aws_iam_policy_document.github_runner_execution_assume_role.json
}

resource "aws_iam_role_policy" "github_runner_execution_role_policy" {
  name = "github_runner_execution_role_policy"
  role = aws_iam_role.github_runner_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = [
          aws_cloudwatch_log_group.github_runner.arn,
          "${aws_cloudwatch_log_group.github_runner.arn}*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
        ]
        Resource = "*"
      }
    ]
  })
}


resource "aws_cloudwatch_log_group" "github_runner" {
  name              = "/github-runner/"
  retention_in_days = 1
}

resource "aws_ecs_task_definition" "github_runner" {
  family = "github-runner"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  cpu = 1024
  memory = 2048
  execution_role_arn = aws_iam_role.github_runner_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "runner"
      image     = "ghcr.io/actions/actions-runner:2.321.0"
      essential = true
      entrypoint = ["bash", "-c"]
      portMappings = []
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.github_runner.name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "runner"
        }
      }
    },
  ])

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture = "ARM64"
  }
}
