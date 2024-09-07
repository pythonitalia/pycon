locals {
  env_vars = [
    {
      name = "VIRTUAL_ENV",
      value = "/var/pretix/venv"
    },
    {
      name = "PATH",
      value = "/var/pretix/venv/bin:/usr/local/bin:/usr/bin:/bin"
    },
        {
          name  = "DATABASE_NAME"
          value = "pretix"
        },
        {
          name  = "DATABASE_USERNAME"
          value = data.aws_db_instance.database.master_username
        },
        {
          name  = "DATABASE_PASSWORD"
          value = module.common_secrets.value.database_password
        },
        {
          name  = "DATABASE_HOST"
          value = data.aws_db_instance.database.address
        },
        {
          name  = "MAIL_USER"
          value = module.secrets.value.mail_user
        },
        {
          name  = "MAIL_PASSWORD"
          value = module.secrets.value.mail_password
        },
        {
          name  = "PRETIX_SENTRY_DSN"
          value = module.secrets.value.sentry_dsn
        },
        {
          name  = "SECRET_KEY"
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
          value = "https://tickets.pycon.it/"
        },
        {
          name  = "PRETIX_PRETIX_TRUST_X_FORWARDED_PROTO",
          value = "true"
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
      environment = local.env_vars
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 0
        }
      ]

      entrypoint = ["/var/pretix/venv/bin/gunicorn"]
      command = ["pretix.wsgi", "--name pretix", "--bind 0.0.0.0:8000",]

      workingDirectory = "/var/pretix"

      dockerLabels = {
        "traefik.enable" = "true"
        "traefik.http.routers.backend.rule" = "Host(`tickets.pycon.it`)"
      }
      mountPoints = [
        {
          sourceVolume  = "media"
          containerPath = "/data/media"
        },
        {
          sourceVolume  = "data"
          containerPath = "/var/pretix-data"
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
          "awslogs-group"         = aws_cloudwatch_log_group.pretix.name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    },
  ])

  volume {
    name      = "media"
    host_path = "/var/pretix/data/media"
  }

  volume {
    name      = "data"
    host_path = "/var/pretix-data"
  }

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
