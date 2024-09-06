resource "aws_cloudwatch_log_group" "traefik" {
  name              = "/ecs/pythonit-${terraform.workspace}-traefik"
  retention_in_days = 3
}

resource "aws_ecs_task_definition" "traefik" {
  family = "pythonit-${terraform.workspace}-traefik"
  container_definitions = jsonencode([
    {
      name              = "traefik"
      image             = "traefik:v3.1.2"
      memoryReservation = 200
      essential         = true

      environment = [
        {
          name = "TRAEFIK_PROVIDERS_ECS_CLUSTERS"
          value = aws_ecs_cluster.server.name
        },
        {
          name = "TRAEFIK_PROVIDERS_ECS_AUTODISCOVERCLUSTERS"
          value = "false",
        },
        {
          name = "TRAEFIK_PROVIDERS_ECS_EXPOSEDBYDEFAULT",
          value = "false",
        },
        {
          name = "TRAEFIK_ENTRYPOINTS_WEB_ADDRESS",
          value = ":80"
        },
      ]

      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        },
      ]

      mountPoints = []
      systemControls = [
        {
          "namespace" : "net.core.somaxconn",
          "value" : "4096"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.traefik.name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }

      healthCheck = {
        retries = 3
        command = [
          "CMD-SHELL",
          "echo 4"
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

resource "aws_ecs_service" "traefik" {
  name                               = "traefik"
  cluster                            = aws_ecs_cluster.server.id
  task_definition                    = aws_ecs_task_definition.traefik.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  lifecycle {
    ignore_changes = [
      capacity_provider_strategy
    ]
  }
}
