locals {
  is_prod = terraform.workspace == "production"
  alias   = local.is_prod ? "frontend.pycon.it" : "${terraform.workspace}-frontend.pycon.it"
  admin_host   = local.is_prod ? "admin.pycon.it" : "${terraform.workspace}-admin.pycon.it"
}

resource "aws_ecs_task_definition" "pycon_frontend" {
  family = "pythonit-${terraform.workspace}-pycon-frontend"

  container_definitions = jsonencode([
    {
      name              = "frontend"
      image             = "${aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.image.image_digest}"
      memoryReservation = local.is_prod ? 400 : 10
      essential         = true

      dockerLabels = {
        "traefik.enable"                        = "true"
        "traefik.http.routers.frontend.rule" = "Host(`${local.alias}`) || Host(`2025.pycon.it`)"
        "traefik.http.services.frontend.loadbalancer.healthcheck.path" = "/api/health"
        "traefik.http.services.frontend.loadbalancer.healthcheck.interval" = "10s"
        "traefik.http.services.frontend.loadbalancer.healthcheck.timeout" = "5s"
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
          name  = "REVALIDATE_SECRET"
          value = module.secrets.value.revalidate_secret
        },
        {
          name  = "CMS_ADMIN_HOST"
          value = local.admin_host
        },
        {
          name = "API_URL_SERVER",
          value = "http://${var.server_ip}"
        },
        {
          name = "REDIS_URL",
          value = "redis://${var.server_ip}/3"
        },
        {
          name = "GIT_HASH",
          value = data.external.githash.result.githash
        },
        {
          name = "SENTRY_AUTH_TOKEN",
          value = module.common_secrets.value.sentry_auth_token
        },
        {
          name = "SENTRY_DSN",
          value = module.secrets.value.sentry_dsn
        },
        {
          name = "NEXT_PUBLIC_POSTHOG_KEY",
          value = module.secrets.value.posthog_key
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
          "curl -s -f http://localhost:3000/api/health || exit 1"
        ]
        timeout  = 5
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
