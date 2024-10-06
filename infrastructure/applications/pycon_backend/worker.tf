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
      value = local.is_prod ? "redis://${data.aws_instance.redis.private_ip}/8" : "redis://${data.aws_instance.redis.private_ip}/13"
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
      value = local.is_prod ? "redis://${data.aws_instance.redis.private_ip}/5" : "redis://${data.aws_instance.redis.private_ip}/14"
    },
    {
      name  = "CELERY_RESULT_BACKEND",
      value = local.is_prod ? "redis://${data.aws_instance.redis.private_ip}/6" : "redis://${data.aws_instance.redis.private_ip}/15"
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

resource "aws_iam_role_policy_attachment" "volume_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSInfrastructureRolePolicyForVolumes"
  role       = aws_iam_role.ecs_service.name
}

resource "aws_ecs_cluster" "worker" {
  name = "pythonit-${terraform.workspace}-worker"
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


data "template_file" "user_data" {
  template = file("${path.module}/user_data.sh")
  vars = {
    ecs_cluster = aws_ecs_cluster.worker.name
  }
}


resource "aws_instance" "instance_1" {
  ami               = var.ecs_arm_ami
  instance_type     = local.is_prod ? "t4g.micro" : "t4g.nano"
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

  dynamic "instance_market_options" {
    for_each = terraform.workspace == "production" ? [] : [1]

    content {
      market_type = "spot"

      spot_options {
        max_price = 0.0031
        spot_instance_type = "persistent"
        instance_interruption_behavior = "stop"
      }
    }
  }

  root_block_device {
    volume_size = 20
  }

  tags = {
    Name = "pythonit-${terraform.workspace}-worker"
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

resource "aws_ecs_service" "beat" {
  name                               = "pythonit-${terraform.workspace}-beat"
  cluster                            = aws_ecs_cluster.worker.id
  task_definition                    = aws_ecs_task_definition.beat.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
