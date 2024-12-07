locals {
  is_prod = terraform.workspace == "production"
  alias   = local.is_prod ? "tickets.pycon.it" : "${terraform.workspace}-tickets.pycon.it"
}

data "aws_db_instance" "database" {
  db_instance_identifier = "pythonit-${terraform.workspace}"
}

resource "aws_ecs_task_definition" "pretix" {
  family = "${terraform.workspace}-pretix"
  container_definitions = jsonencode([
    {
      name              = "pretix"
      image             = "${data.aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.image.image_digest}"
      memoryReservation = local.is_prod ? 1840 : 10
      essential         = true

      dockerLabels = {
        "traefik.enable"                        = "true"
        "traefik.http.routers.pretix-web.rule" = "Host(`${local.alias}`)"
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
          value = data.aws_db_instance.database.master_username
        },
        {
          name  = "PRETIX_DATABASE_PASSWORD"
          value = module.common_secrets.value.database_password
        },
        {
          name  = "PRETIX_DATABASE_HOST"
          value = data.aws_db_instance.database.address
        },
        {
          name  = "PRETIX_DATABASE_PORT"
          value = "5432"
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

      healthCheck = {
        retries = 3
        command = [
          "CMD-SHELL",
          "curl -f http://localhost/healthcheck/ || exit 1"
        ]
        timeout  = 3
        interval = 10
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
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
