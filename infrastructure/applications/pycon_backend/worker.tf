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
      value = "admin.pycon.it"
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
      name  = "PYTHONIT_EMAIL_BACKEND",
      value = "pythonit_toolkit.emails.backends.ses.SESEmailBackend"
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
      name  = "PINPOINT_APPLICATION_ID",
      value = module.secrets.value.pinpoint_application_id
    },
    {
      name  = "SQS_QUEUE_URL",
      value = aws_sqs_queue.queue.id
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
      name  = "AZURE_STORAGE_ACCOUNT_NAME",
      value = module.secrets.value.azure_storage_account_name
    },
    {
      name  = "AZURE_STORAGE_ACCOUNT_KEY",
      value = module.secrets.value.azure_storage_account_key
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
      value = local.is_prod ? "redis://${data.aws_elasticache_cluster.redis.cache_nodes.0.address}/8" : "locmemcache://snowflake"
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
      name  = "DEEPL_AUTH_KEY",
      value = module.secrets.value.deepl_auth_key
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
      value = "redis://${data.aws_elasticache_cluster.redis.cache_nodes.0.address}/5"
    },
    {
      name  = "CELERY_RESULT_BACKEND",
      value = "redis://${data.aws_elasticache_cluster.redis.cache_nodes.0.address}/6"
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
  ]
}
resource "aws_ecs_cluster" "worker" {
  name = "pythonit-${terraform.workspace}-worker"
}

data "aws_ami" "ecs" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn-ami-*-amazon-ecs-optimized"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["amazon"]
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


data "template_file" "user_data" {
  template = file("${path.module}/user_data.sh")
  vars = {
    ecs_cluster = aws_ecs_cluster.worker.name
  }
}


resource "aws_instance" "instance" {
  ami               = "ami-05ff3e0fe4cf2c226"
  instance_type     = "t3a.small"
  subnet_id         = data.aws_subnet.private_1a.id
  availability_zone = "eu-central-1a"
  vpc_security_group_ids = [
    data.aws_security_group.rds.id,
    data.aws_security_group.lambda.id,
    aws_security_group.instance.id
  ]
  source_dest_check    = false
  user_data            = data.template_file.user_data.rendered
  iam_instance_profile = aws_iam_instance_profile.worker.name
  key_name             = "pretix"

  tags = {
    Name = "pythonit-${terraform.workspace}-worker"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_cloudwatch_log_group" "worker_logs" {
  name              = "/ecs/pythonit-${terraform.workspace}-worker"
  retention_in_days = 7
}


resource "aws_ecs_task_definition" "worker" {
  family = "pythonit-${terraform.workspace}-worker"
  container_definitions = jsonencode([
    {
      name      = "worker"
      image     = "${data.aws_ecr_repository.be_repo.repository_url}@${data.aws_ecr_image.be_image.image_digest}"
      cpu       = 1024
      memory    = 975
      essential = true
      entrypoint = [
        "/home/app/.venv/bin/celery",
      ]

      command = [
        "-A", "pycon", "worker", "-c", "2", "-l", "info"
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
          "awslogs-group"         = aws_cloudwatch_log_group.worker_logs.name
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
    },
    {
      name      = "beat"
      image     = "${data.aws_ecr_repository.be_repo.repository_url}@${data.aws_ecr_image.be_image.image_digest}"
      cpu       = 1024
      memory    = 975
      essential = true
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
          "awslogs-group"         = aws_cloudwatch_log_group.worker_logs.name
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

      stopTimeout = 30
    }
  ])

  requires_compatibilities = []
  tags                     = {}
}

resource "aws_ecs_service" "worker" {
  name                               = "pythonit-${terraform.workspace}-worker"
  cluster                            = aws_ecs_cluster.worker.id
  task_definition                    = aws_ecs_task_definition.worker.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
