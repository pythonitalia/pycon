locals {
  is_prod = terraform.workspace == "production"
  alias   = local.is_prod ? "frontend.pycon.it" : "${terraform.workspace}-frontend.pycon.it"
}

resource "aws_ecs_task_definition" "pycon_frontend" {
  family = "pythonit-${terraform.workspace}-pycon-frontend"

  container_definitions = jsonencode([
    {
      name              = "frontend"
      image             = "${data.aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.image.image_digest}"
      memoryReservation = 400
      essential         = true

      dockerLabels = {
        "traefik.enable"                        = "true"
        "traefik.http.routers.frontend.rule" = "Host(`${local.alias}`)"
      }

      environment = [
        {
          name  = "CMS_HOSTNAME"
          value = module.secrets.value.cms_hostname
        },
        {
          name  = "CONFERENCE_CODE"
          value = module.secrets.value.conference_code
        },
        {
          name = "API_URL_SERVER",
          # value = "http://${var.server_ip}"
          value = local.is_prod ? "https://admin.pycon.it" : "https://pastaporto-admin.pycon.it"
        }
      ]

      portMappings = [
        {
          containerPort = 3000
          hostPort      = 0
        },
      ]

      mountPoints = []

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = var.logs_group_name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "frontend"
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

resource "aws_ecs_service" "frontend" {
  name                               = "frontend"
  cluster                            = var.cluster_id
  task_definition                    = aws_ecs_task_definition.pycon_frontend.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200
}
