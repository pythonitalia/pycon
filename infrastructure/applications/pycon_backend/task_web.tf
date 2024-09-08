data "aws_ecs_cluster" "server" {
  cluster_name = "${terraform.workspace}-server"
}

resource "aws_cloudwatch_log_group" "backend" {
  name              = "/ecs/pythonit-${terraform.workspace}-backend"
  retention_in_days = 3
}

resource "aws_ecs_task_definition" "backend" {
  family = "pythonit-${terraform.workspace}-backend"
  container_definitions = jsonencode([
    {
      name              = "backend"
      image             = "${data.aws_ecr_repository.be_repo.repository_url}@${data.aws_ecr_image.be_arm_image.image_digest}"
      memoryReservation = 200
      essential         = true

      entrypoint = [
        "/home/app/.venv/bin/uwsgi",
      ]

      command = [
        "--http", ":8000", "--module", "pycon.wsgi:application"
      ]

      dockerLabels = {
        "traefik.enable" = "true"
        "traefik.http.routers.backend-web.rule" = "Host(`${local.web_domain}`)"
      }

      environment = local.env_vars
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 0
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
          "awslogs-group"         = aws_cloudwatch_log_group.backend.name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "ecs"
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


resource "aws_ecs_service" "backend" {
  name                               = "backend-web"
  cluster                            = data.aws_ecs_cluster.server.id
  task_definition                    = aws_ecs_task_definition.backend.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  lifecycle {
    ignore_changes = [
      capacity_provider_strategy
    ]
  }
}
