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


resource "aws_instance" "pretix" {
  ami               = data.aws_ami.ecs.id
  instance_type     = "t3a.micro"
  subnet_id         = data.aws_subnet.private_1a.id
  availability_zone = "eu-central-1a"
  vpc_security_group_ids = [
    data.aws_security_group.rds.id,
    data.aws_security_group.lambda.id
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

resource "aws_ecs_task_definition" "worker" {
  family = "pythonit-${terraform.workspace}-worker"
  container_definitions = jsonencode([
    {
      name      = "worker"
      image     = "${data.aws_ecr_repository.be_repo.repository_url}@${data.aws_ecr_image.be_image.image_digest}"
      cpu       = 2048
      memory    = 1000
      essential = true
      entrypoint = [
        "/home/app/.venv/bin/python",
        "-m",
        "celery"
      ]

      command = [
        "multi", "start", "2", "-c", "2",
      ]

      environment = [
        {
          name= "DATABASE_URL",
          value =                 local.db_connection
          },
        {
          name= "DEBUG",
          value =                        "False"
          },
        {
          name= "SECRET_KEY",
          value =                   module.secrets.value.secret_key
          },
        {
          name= "MAPBOX_PUBLIC_API_KEY",
          value =        module.secrets.value.mapbox_public_api_key
          },
        {
          name= "SENTRY_DSN",
          value =                   module.secrets.value.sentry_dsn
          },
        {
          name= "VOLUNTEERS_PUSH_NOTIFICATIONS_IOS_ARN",
          value =     module.secrets.value.volunteers_push_notifications_ios_arn
          },
        {
          name= "VOLUNTEERS_PUSH_NOTIFICATIONS_ANDROID_ARN",
          value = module.secrets.value.volunteers_push_notifications_android_arn
          },
        {
          name= "ALLOWED_HOSTS",
          value =                "*"
          },
        {
          name= "DJANGO_SETTINGS_MODULE",
          value =       "pycon.settings.prod"
          },
        {
          name= "ASSOCIATION_FRONTEND_URL",
          value =     "https://associazione.python.it"
          },
        {
          name= "AWS_MEDIA_BUCKET",
          value =             aws_s3_bucket.backend_media.id
          },
        {
          name= "AWS_REGION_NAME",
          value =              aws_s3_bucket.backend_media.region
          },
        {
          name= "SPEAKERS_EMAIL_ADDRESS",
          value =       module.secrets.value.speakers_email_address
          },
        {
          name= "EMAIL_BACKEND",
          value =                "django_ses.SESBackend"
          },
        {
          name= "PYTHONIT_EMAIL_BACKEND",
          value =       "pythonit_toolkit.emails.backends.ses.SESEmailBackend"
          },
        {
          name= "FRONTEND_URL",
          value =                 "https://pycon.it"
          },
        {
          name= "PRETIX_API",
          value =                   "https://tickets.pycon.it/api/v1/"
          },
        {
          name= "AWS_S3_CUSTOM_DOMAIN",
          value =             local.cdn_url
          },
        {
          name= "PRETIX_API_TOKEN",
          value =                 module.common_secrets.value.pretix_api_token
          },
        {
          name= "PINPOINT_APPLICATION_ID",
          value =          module.secrets.value.pinpoint_application_id
          },
        {
          name= "FORCE_PYCON_HOST",
          value =                 local.is_prod
          },
        {
          name= "SQS_QUEUE_URL",
          value =                    aws_sqs_queue.queue.id
          },
        {
          name= "MAILCHIMP_SECRET_KEY",
          value =             module.common_secrets.value.mailchimp_secret_key
          },
        {
          name= "MAILCHIMP_DC",
          value =                     module.common_secrets.value.mailchimp_dc
          },
        {
          name= "MAILCHIMP_LIST_ID",
          value =                module.common_secrets.value.mailchimp_list_id
          },
        {
          name= "USER_ID_HASH_SALT",
          value =                module.secrets.value.userid_hash_salt
          },
        {
          name= "AZURE_STORAGE_ACCOUNT_NAME",
          value =       module.secrets.value.azure_storage_account_name
          },
        {
          name= "AZURE_STORAGE_ACCOUNT_KEY",
          value =        module.secrets.value.azure_storage_account_key
          },
        {
          name= "PLAIN_API",
          value =                        "https://core-api.uk.plain.com/graphql/v1"
          },
        {
          name= "PLAIN_API_TOKEN",
          value =                  module.secrets.value.plain_api_token
          },
        {
          name= "CACHE_URL",
          value =                        local.is_prod ? "redis://${data.aws_elasticache_cluster.redis.cache_nodes.0.address}/8" : "locmemcache://snowflake"
          },
        {
          name= "TEMPORAL_ADDRESS",
          value =                 var.deploy_temporal ? "${data.aws_instance.temporal_machine[0].private_ip}:7233" : ""
          },
        {
          name= "STRIPE_WEBHOOK_SIGNATURE_SECRET",
          value =  module.secrets.value.stripe_webhook_secret
          },
        {
          name= "STRIPE_SUBSCRIPTION_PRICE_ID",
          value =     module.secrets.value.stripe_membership_price_id
          },
        {
          name= "STRIPE_SECRET_API_KEY",
          value =            module.secrets.value.stripe_secret_api_key
          },
        {
          name= "PRETIX_WEBHOOK_SECRET",
          value =            module.secrets.value.pretix_webhook_secret
          },
        {
          name= "DEEPL_AUTH_KEY",
          value =                   module.secrets.value.deepl_auth_key
          },
        {
          name= "FLODESK_API_KEY",
          value =                  module.secrets.value.flodesk_api_key
          },
        {
          name= "FLODESK_SEGMENT_ID",
          value =               module.secrets.value.flodesk_segment_id
          }

      ]

      mountPoints = []
      systemControls = [
        {
          "namespace" : "net.core.somaxconn",
          "value" : "4096"
        }
      ]
    },
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
