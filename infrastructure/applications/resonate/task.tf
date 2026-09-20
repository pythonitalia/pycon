locals {
  is_prod = terraform.workspace == "production"

  # Resonate keeps its promises on the database instance the backend already
  # uses, in a database of its own.
  database = "resonate"

  database_url = "postgres://${var.database_settings.username}:${var.database_settings.password}@${var.database_settings.address}:${var.database_settings.port}/${local.database}?sslmode=require"
}

resource "aws_ecs_task_definition" "resonate" {
  family = "pythonit-${terraform.workspace}-resonate"

  container_definitions = jsonencode([
    {
      # The instance is private, so Terraform cannot create the database
      # itself. This runs before the server on every deploy and does nothing
      # after the first one.
      name              = "create-database"
      image             = "postgres:18-alpine"
      memoryReservation = 10
      essential         = false

      command = [
        "sh", "-c", "createdb ${local.database} || true"
      ]

      environment = [
        {
          name  = "PGHOST"
          value = var.database_settings.address
        },
        {
          name  = "PGPORT"
          value = tostring(var.database_settings.port)
        },
        {
          name  = "PGUSER"
          value = var.database_settings.username
        },
        {
          name  = "PGPASSWORD"
          value = var.database_settings.password
        },
        {
          # Where to connect to issue the CREATE DATABASE, not what to create.
          name  = "PGDATABASE"
          value = var.database_settings.db_name
        },
        {
          name  = "PGSSLMODE"
          value = "require"
        }
      ]

      mountPoints    = []
      systemControls = []

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = var.logs_group_name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "resonate-create-database"
        }
      }
    },
    {
      name              = "resonate"
      image             = "resonatehqio/resonate:v0.9.8"
      memoryReservation = local.is_prod ? 200 : 10
      essential         = true

      dependsOn = [
        {
          containerName = "create-database"
          condition     = "SUCCESS"
        }
      ]

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
        retries = 3
        command = [
          "CMD-SHELL",
          "wget -qO- http://127.0.0.1:8001/health || exit 1"
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

resource "aws_ecs_service" "resonate" {
  name                               = "resonate"
  cluster                            = var.cluster_id
  task_definition                    = aws_ecs_task_definition.resonate.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
