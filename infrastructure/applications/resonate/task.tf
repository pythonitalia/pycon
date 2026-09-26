locals {
  is_prod = terraform.workspace == "production"

  # Resonate keeps its promises on the database instance the backend already
  # uses, in a database of its own. The instance is private, so that database
  # is not created from here: it has to exist before this runs.
  database = "resonate"

  database_url = "postgres://${var.database_settings.username}:${var.database_settings.password}@${var.database_settings.address}:${var.database_settings.port}/${local.database}?sslmode=require"
}

resource "aws_ecs_task_definition" "resonate" {
  family = "pythonit-${terraform.workspace}-resonate"

  container_definitions = jsonencode([
    {
      name              = "resonate"
      image             = "resonatehqio/resonate:v0.9.8"
      memoryReservation = local.is_prod ? 200 : 10
      essential         = true

      environment = [
        {
          name  = "RESONATE_SERVER__BIND"
          value = "0.0.0.0"
        },
        {
          name  = "RESONATE_STORAGE__TYPE"
          value = "postgres"
        },
        {
          name  = "RESONATE_STORAGE__POSTGRES__URL"
          value = local.database_url
        }
      ]

      portMappings = [
        {
          containerPort = 8001
          hostPort      = 8001
          name          = "resonate"
        }
      ]

      mountPoints    = []
      systemControls = []

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = var.logs_group_name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "resonate"
        }
      }

      healthCheck = {
        retries = 10
        command = [
          "CMD-SHELL",
          "wget -qO- http://127.0.0.1:8001/health || exit 1"
        ]
        timeout  = 3
        interval = 10
        # The server spends up to 30 seconds waiting on the database pool
        # before it gives up, and creates its schema on first boot, so it
        # needs more room than the default none before checks start counting.
        startPeriod = 60
      }

      stopTimeout = 300
    }
  ])

  requires_compatibilities = []
  tags                     = {}
}

resource "aws_ecs_service" "resonate" {
  name                               = "resonate"
  cluster                            = var.cluster_id
  task_definition                    = aws_ecs_task_definition.resonate.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
