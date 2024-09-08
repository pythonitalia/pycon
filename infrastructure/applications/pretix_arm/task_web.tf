locals {
  domain = local.is_prod ? "tickets.pycon.it" : "${terraform.workspace}-tickets.pycon.it"

  env_vars = [
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
      name  = "PRETIX_PRETIX_TRUST_X_FORWARDED_HOST"
      value = "true"
    },
    {
      name  = "PRETIX_PRETIX_REGISTRATION"
      value = "true"
    },
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
      value = "redis://${data.aws_instance.redis.private_ip}/0"
    },
    {
      name  = "PRETIX_REDIS_SESSIONS",
      value = "false"
    },
    {
      name  = "PRETIX_CELERY_BROKER",
      value = "redis://${data.aws_instance.redis.private_ip}/1"
    },
    {
      name  = "PRETIX_CELERY_BACKEND",
      value = "redis://${data.aws_instance.redis.private_ip}/2"
    },
    {
      name  = "PRETIX_PRETIX_URL",
      value = "https://${local.domain}/"
    },
    {
      name  = "PRETIX_PRETIX_TRUST_X_FORWARDED_PROTO",
      value = "true"
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
      name = "PRETIX_PYCON_STORAGE_BUCKET_NAME",
      value = aws_s3_bucket.media.bucket
    }
  ]
}
data "aws_ecs_cluster" "server" {
  cluster_name = "${terraform.workspace}-server"
}

data "aws_instance" "redis" {
  instance_tags = {
    Name = "pythonit-production-redis"
  }

  filter {
    name   = "instance-state-name"
    values = ["running"]
  }
}

resource "aws_cloudwatch_log_group" "pretix" {
  name              = "/ecs/pythonit-${terraform.workspace}-pretix-arm"
  retention_in_days = 7
}

resource "aws_ecs_task_definition" "pretix_web" {
  family = "pythonit-${terraform.workspace}-pretix"
  container_definitions = jsonencode([
    {
      name              = "pretix"
      image             = "${data.aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.image.image_digest}"
      memoryReservation = 200
      essential         = true
      environment       = local.env_vars
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 0
        }
      ]

      entrypoint       = ["gunicorn"]
      command          = [
        "pretix.wsgi", "--name=pretix", "--bind=0.0.0.0:8000", "--max-requests=1200", "--max-requests-jitter=50",
        "--workers=4"
      ]
      workingDirectory = "/pretix/src"
      user             = "pretixuser"

      dockerLabels = {
        "traefik.enable" = "true"
        "traefik.http.routers.pretix-web.rule" = "Host(`${local.domain}`)"
      }

      systemControls = [
        {
          "namespace" : "net.core.somaxconn",
          "value" : "4096"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.pretix.name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    },
  ])

  requires_compatibilities = []
  tags                     = {}
}

resource "aws_ecs_service" "pretix_web" {
  name                               = "pretix-web"
  cluster                            = data.aws_ecs_cluster.server.id
  task_definition                    = aws_ecs_task_definition.pretix_web.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  lifecycle {
    ignore_changes = [
      capacity_provider_strategy
    ]
  }
}
