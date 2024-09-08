resource "aws_cloudwatch_log_group" "pretix_worker" {
  name              = "/ecs/pythonit-${terraform.workspace}-pretix-worker"
  retention_in_days = 7
}

resource "aws_ecs_task_definition" "pretix_worker" {
  family = "pythonit-${terraform.workspace}-pretix-worker"
  container_definitions = jsonencode([
    {
      name              = "worker"
      image             = "${data.aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.image.image_digest}"
      memoryReservation = 200
      essential         = true
      environment       = local.env_vars

      entrypoint       = ["pretix"]
      command          = ["taskworker"]

      workingDirectory = "/pretix/src"
      user             = "pretixuser"

      healthCheck = {
        retries = 3
        command = [
          "CMD-SHELL",
          "celery -A pretix.celery_app inspect ping"
        ]
        timeout  = 3
        interval = 10
      }

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.pretix_worker.name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    },
    {
      name              = "cron"
      image             = "${data.aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.image.image_digest}"
      memoryReservation = 200
      essential         = true
      environment       = local.env_vars

      entrypoint       = ["bash", "-c"]
      command          = ["while true; do pretix cron; sleep 60; done"]

      healthCheck = {
        retries = 3
        command = [
          "CMD-SHELL",
          "echo 1"
        ]
        timeout  = 3
        interval = 10
      }

      workingDirectory = "/pretix/src"
      user             = "pretixuser"

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.pretix_worker.name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    },
  ])

  requires_compatibilities = []
  tags                     = {}
}

resource "aws_ecs_service" "pretix_worker" {
  name                               = "pretix-worker"
  cluster                            = data.aws_ecs_cluster.server.id
  task_definition                    = aws_ecs_task_definition.pretix_worker.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  lifecycle {
    ignore_changes = [
      capacity_provider_strategy
    ]
  }
}
