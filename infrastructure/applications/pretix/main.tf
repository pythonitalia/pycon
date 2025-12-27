locals {
  is_prod = terraform.workspace == "production"
  alias   = local.is_prod ? "tickets.pycon.it" : "${terraform.workspace}-tickets.pycon.it"
}

resource "aws_ecs_task_definition" "pretix" {
  family = "${terraform.workspace}-pretix"
  container_definitions = jsonencode([
    {
      name              = "pretix"
      image             = "${data.aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.image.image_digest}"
      memoryReservation = local.is_prod ? 1500 : 10
      essential         = true

      dockerLabels = {
        "traefik.enable"                        = "true"
        "traefik.http.routers.pretix-web.rule" = "Host(`${local.alias}`)"
        "traefik.http.services.pretix-web.loadbalancer.healthcheck.path" = "/healthcheck/"
        "traefik.http.services.pretix-web.loadbalancer.healthcheck.interval" = "10s"
        "traefik.http.services.pretix-web.loadbalancer.healthcheck.timeout" = "5s"
        "traefik.http.services.pretix-web.loadbalancer.healthcheck.hostname" = local.alias
      }

      healthCheck = {
        retries = 3
        command = [
          "CMD-SHELL",
          "curl -s --header 'Host: ${local.alias}' -f http://127.0.0.1/healthcheck/ || exit 1"
        ]
        timeout  = 5
        interval = 10
        startPeriod = 120
      }

      environment = [
        {
          name  = "PRETIX_SENTRY_DSN"
          value = module.secrets.value.sentry_dsn
        },
        {
          name  = "PRETIX_DJANGO_SECRET"
          value = module.secrets.value.secret_key
        },
        {
          name  = "PRETIX_REDIS_LOCATION",
          value = "redis://${var.server_ip}/0"
        },
        {
          name  = "PRETIX_REDIS_SESSIONS",
          value = "false"
        },
        {
          name  = "PRETIX_CELERY_BROKER",
          value = "redis://${var.server_ip}/1"
        },
        {
          name  = "PRETIX_CELERY_BACKEND",
          value = "redis://${var.server_ip}/2"
        },
        {
          name  = "PRETIX_PRETIX_URL",
          value = "https://${local.alias}/"
        },
        {
          name  = "PRETIX_PRETIX_TRUST_X_FORWARDED_PROTO",
          value = "true"
        },
        {
          name  = "VIRTUAL_ENV",
          value = "/var/pretix/venv"
        },
        {
          name  = "PATH",
          value = "/var/pretix/venv/bin:/usr/local/bin:/usr/bin:/bin"
        },
        {
          name  = "PRETIX_DATABASE_BACKEND",
          value = "postgresql"
        },
        {
          name  = "PRETIX_DATABASE_NAME"
          value = "pretix"
        },
        {
          name  = "PRETIX_DATABASE_USER"
          value = var.database_settings.username
        },
        {
          name  = "PRETIX_DATABASE_PASSWORD"
          value = var.database_settings.password
        },
        {
          name  = "PRETIX_DATABASE_HOST"
          value = var.database_settings.address
        },
        {
          name  = "PRETIX_DATABASE_PORT"
          value = tostring(var.database_settings.port)
        },
        {
          name  = "PRETIX_DATABASE_SSLMODE"
          value = "require"
        },
        {
          name  = "PRETIX_MAIL_USER"
          value = module.secrets.value.mail_user
        },
        {
          name  = "PRETIX_MAIL_PASSWORD"
          value = module.secrets.value.mail_password
        },
        {
          name  = "PRETIX_MAIL_HOST"
          value = "email-smtp.eu-central-1.amazonaws.com"
        },
        {
          name  = "PRETIX_MAIL_PORT"
          value = "587"
        },
        {
          name  = "PRETIX_MAIL_TLS"
          value = "true"
        },
        {
          name  = "PRETIX_MAIL_SSL"
          value = "false"
        },
        {
          name  = "PRETIX_MAIL_FROM"
          value = "noreply@pycon.it"
        },
        {
          # this is is needed for our hack that updates the order view
          # without having to rewrite the whole template
          name  = "PRETIX_PRETIX_CSP_ADDITIONAL_HEADER",
          value = "script-src 'self' 'unsafe-inline'"
        },
        {
          name  = "PRETIX_PRETIX_INSTANCE_NAME",
          value = "Python Italia"
        },
        {
          name = "DJANGO_SETTINGS_MODULE",
          value = "production_settings"
        },
        {
          name = "DATA_DIR",
          value = "/data/"
        },
        {
          name = "HOME",
          value = "/pretix"
        },
        {
          name = "PRETIX_PYCON_MEDIA_BUCKET_NAME",
          value = aws_s3_bucket.media.bucket
        },
        {
          name = "AWS_S3_REGION_NAME",
          value = "eu-central-1"
        },
        {
          name = "AWS_REQUEST_CHECKSUM_CALCULATION",
          value = "WHEN_REQUIRED"
        },
        {
          name = "AWS_RESPONSE_CHECKSUM_VALIDATION",
          value = "WHEN_REQUIRED"
        }
      ]
      portMappings = [
        {
          containerPort = 80
          hostPort      = 0
        }
      ]
      systemControls = [
        {
          "namespace" : "net.core.somaxconn",
          "value" : "4096"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = var.logs_group_name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "pretix"
        }
      }
    },
  ])

  requires_compatibilities = []
  tags                     = {}
}

resource "aws_ecs_service" "pretix" {
  name                               = "pretix"
  cluster                            = var.cluster_id
  task_definition                    = aws_ecs_task_definition.pretix.arn
  desired_count                      = local.is_prod ? 1 : 0
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200
}
