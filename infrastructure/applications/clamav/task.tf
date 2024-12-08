locals {
  is_prod = terraform.workspace == "production"
}

resource "aws_ecs_task_definition" "clamav" {
  family = "pythonit-${terraform.workspace}-clamav"

  container_definitions = jsonencode([
    {
      name              = "clamav"
      image             = "clamav/clamav-debian:1.4.1"
      memoryReservation = local.is_prod ? 1000 : 10
      essential         = true

      portMappings = [
        {
          containerPort = 3310
          hostPort      = 3310
        },
      ]

      mountPoints = []

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = var.logs_group_name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "clamav"
        }
      }

      healthCheck = {
        retries = 3
        command = [
          "CMD-SHELL",
          "echo 1"
        ]
        timeout  = 3
        interval = 10
      }

      stopTimeout = 300
    }
  ])

  requires_compatibilities = []
  tags                     = {}
}

resource "aws_ecs_service" "clamav" {
  name                               = "clamav"
  cluster                            = var.cluster_id
  task_definition                    = aws_ecs_task_definition.clamav.arn
  desired_count                      = local.is_prod ? 1 : 0
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
