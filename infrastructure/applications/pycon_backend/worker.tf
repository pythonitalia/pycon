locals {
  env_vars = [
    {
      name  = "DATABASE_URL",
      value = local.db_connection
    },
    {
      name  = "DEBUG",
      value = "False"
    },
    {
      name  = "SECRET_KEY",
      value = module.secrets.value.secret_key
    },
    {
      name  = "MAPBOX_PUBLIC_API_KEY",
      value = module.secrets.value.mapbox_public_api_key
    },
    {
      name  = "SENTRY_DSN",
      value = module.secrets.value.sentry_dsn
    },
    {
      name  = "VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN",
      value = module.secrets.value.volunteers_push_notifications_ios_arn
    },
    {
      name  = "VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN",
      value = module.secrets.value.volunteers_push_notifications_android_arn
    },
    {
      name  = "ALLOWED_HOSTS",
      value = ".pycon.it"
    },
    {
      name  = "DJANGO_SETTINGS_MODULE",
      value = "pycon.settings.prod"
    },
    {
      name  = "ASSOCIATION_FRONTEND_URL",
      value = "https://associazione.python.it"
    },
    {
      name  = "AWS_MEDIA_BUCKET",
      value = aws_s3_bucket.backend_media.id
    },
    {
      name  = "AWS_REGION_NAME",
      value = aws_s3_bucket.backend_media.region
    },
    {
      name  = "AWS_DEFAULT_REGION",
      value = "eu-central-1"
    },
    {
      name  = "SPEAKERS_EMAIL_ADDRESS",
      value = module.secrets.value.speakers_email_address
    },
    {
      name  = "EMAIL_BACKEND",
      value = "django_ses.SESBackend"
    },
    {
      name  = "FRONTEND_URL",
      value = "https://pycon.it"
    },
    {
      name  = "PRETIX_API",
      value = "https://tickets.pycon.it/api/v1/"
    },
    {
      name  = "AWS_S3_CUSTOM_DOMAIN",
      value = local.cdn_url
    },
    {
      name  = "PRETIX_API_TOKEN",
      value = module.common_secrets.value.pretix_api_token
    },
    {
      name  = "MAILCHIMP_SECRET_KEY",
      value = module.common_secrets.value.mailchimp_secret_key
    },
    {
      name  = "MAILCHIMP_DC",
      value = module.common_secrets.value.mailchimp_dc
    },
    {
      name  = "MAILCHIMP_LIST_ID",
      value = module.common_secrets.value.mailchimp_list_id
    },
    {
      name  = "USER_ID_HASH_SALT",
      value = module.secrets.value.userid_hash_salt
    },
    {
      name  = "PLAIN_API",
      value = "https://core-api.uk.plain.com/graphql/v1"
    },
    {
      name  = "PLAIN_API_TOKEN",
      value = module.secrets.value.plain_api_token
    },
    {
      name  = "CACHE_URL",
      value = local.is_prod ? "redis://${var.server_ip}/8" : "redis://${var.server_ip}/13"
    },
    {
      name  = "STRIPE_WEBHOOK_SIGNATURE_SECRET",
      value = module.secrets.value.stripe_webhook_secret
    },
    {
      name  = "STRIPE_SUBSCRIPTION_PRICE_ID",
      value = module.secrets.value.stripe_membership_price_id
    },
    {
      name  = "STRIPE_SECRET_API_KEY",
      value = module.secrets.value.stripe_secret_api_key
    },
    {
      name  = "PRETIX_WEBHOOK_SECRET",
      value = module.secrets.value.pretix_webhook_secret
    },
    {
      name  = "OPENAI_API_KEY",
      value = module.secrets.value.openai_api_key
    },
    {
      name  = "FLODESK_API_KEY",
      value = module.secrets.value.flodesk_api_key
    },
    {
      name  = "FLODESK_SEGMENT_ID",
      value = module.secrets.value.flodesk_segment_id
    },
    {
      name  = "CELERY_BROKER_URL",
      value = local.is_prod ? "redis://${var.server_ip}/5" : "redis://${var.server_ip}/14"
    },
    {
      name  = "CELERY_RESULT_BACKEND",
      value = local.is_prod ? "redis://${var.server_ip}/6" : "redis://${var.server_ip}/15"
    },
    {
      name  = "ENV",
      value = terraform.workspace
    },
    {
      name  = "GITHASH",
      value = data.external.githash.result.githash
    },
    {
      name  = "PLAIN_INTEGRATION_TOKEN"
      value = module.secrets.value.plain_integration_token
    },
    {
      name  = "HASHID_DEFAULT_SECRET_SALT",
      value = module.secrets.value.hashid_default_secret_salt
    },
    {
      name = "MEDIA_FILES_STORAGE_BACKEND",
      value = "pycon.storages.CustomS3Boto3Storage"
    },
    {
      name = "CLAMAV_HOST",
      value = module.secrets.value.clamav_host
    },
    {
      name = "ECS_NETWORK_CONFIG",
      value = jsonencode({
        subnets = [data.aws_subnet.public_1a.id],
        security_groups = [
          data.aws_security_group.rds.id,
          data.aws_security_group.lambda.id,
          aws_security_group.instance.id
        ],
      })
    },
    {
      name = "ECS_SERVICE_ROLE",
      value = aws_iam_role.ecs_service.arn
    },
    {
      name = "AWS_SES_CONFIGURATION_SET"
      value = data.aws_sesv2_configuration_set.main.configuration_set_name
    },
    {
      name = "SNS_WEBHOOK_SECRET",
      value = "module.common_secrets.value.sns_webhook_secret"
    }
  ]
}

resource "aws_iam_role" "ecs_service" {
  name = "pythonit-${terraform.workspace}-ecs-service"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

data "aws_subnet" "private_1a" {
  vpc_id = data.aws_vpc.default.id

  filter {
    name   = "tag:Type"
    values = ["private"]
  }

  filter {
    name   = "tag:AZ"
    values = ["eu-central-1a"]
  }
}

data "aws_subnet" "public_1a" {
  vpc_id = data.aws_vpc.default.id

  filter {
    name   = "tag:Type"
    values = ["public"]
  }

  filter {
    name   = "tag:AZ"
    values = ["eu-central-1a"]
  }
}

resource "aws_ecs_task_definition" "worker" {
  family = "pythonit-${terraform.workspace}-worker"

  container_definitions = jsonencode([
    {
      name              = "worker"
      image             = "${data.aws_ecr_repository.be_repo.repository_url}@${data.aws_ecr_image.be_arm_image.image_digest}"
      memoryReservation = 200
      essential         = true
      entrypoint = [
        "/home/app/.venv/bin/celery",
      ]

      command = [
        "-A", "pycon", "worker", "-l", "info", "-E"
      ]

      environment = local.env_vars

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
          "awslogs-group"         = var.logs_group_name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "backend-worker"
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

resource "aws_ecs_task_definition" "beat" {
  family = "pythonit-${terraform.workspace}-beat"

  container_definitions = jsonencode([
    {
      name              = "beat"
      image             = "${data.aws_ecr_repository.be_repo.repository_url}@${data.aws_ecr_image.be_arm_image.image_digest}"
      memoryReservation = 200
      essential         = true
      entrypoint = [
        "/home/app/.venv/bin/celery",
      ]

      command = [
        "-A", "pycon", "beat", "-l", "info"
      ]

      environment = local.env_vars

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
          "awslogs-group"         = var.logs_group_name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "beat"
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

      stopTimeout = 30
    }
  ])

  requires_compatibilities = []
  tags                     = {}
}

resource "aws_ecs_service" "worker" {
  name                               = "backend-worker"
  cluster                            = var.cluster_id
  task_definition                    = aws_ecs_task_definition.worker.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}

resource "aws_ecs_service" "beat" {
  name                               = "backend-beat"
  cluster                            = var.cluster_id
  task_definition                    = aws_ecs_task_definition.beat.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
