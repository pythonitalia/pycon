data "aws_db_instance" "database" {
  db_instance_identifier = "pythonit-${terraform.workspace}"
}

resource "aws_ecs_cluster" "pretix" {
  name = "${terraform.workspace}-pretix"
}

data "template_file" "user_data" {
  template = file("${path.module}/user_data.sh")
  vars = {
    ecs_cluster = aws_ecs_cluster.pretix.name
  }
}

resource "aws_instance" "pretix" {
  ami               = var.ecs_arm_ami
  instance_type     = "t4g.small"
  subnet_id         = data.aws_subnet.public.id
  availability_zone = "eu-central-1a"
  vpc_security_group_ids = [
    aws_security_group.instance.id,
    data.aws_security_group.rds.id
  ]
  source_dest_check    = false
  user_data            = data.template_file.user_data.rendered
  iam_instance_profile = aws_iam_instance_profile.instance.name
  key_name             = "pretix"

  root_block_device {
    volume_size = 15
  }

  tags = {
    Name = "${terraform.workspace}-pretix-instance"
  }
}

resource "aws_volume_attachment" "data_attachment" {
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.data.id
  instance_id = aws_instance.pretix.id
}

resource "aws_cloudwatch_log_group" "pretix_logs" {
  name              = "/ecs/pythonit-${terraform.workspace}-pretix"
  retention_in_days = 7
}


resource "aws_eip" "ip" {
  instance = aws_instance.pretix.id
  domain   = "vpc"
  tags = {
    Name = "${terraform.workspace}-pretix"
  }
}

data "aws_db_proxy" "proxy" {
  count = var.enable_proxy ? 1 : 0
  name  = "pythonit-${terraform.workspace}-database-proxy"
}

resource "aws_ebs_volume" "data" {
  availability_zone = "eu-central-1a"
  size              = 20
  type              = "gp3"

  tags = {
    Name = "pretix-data"
  }
}

resource "aws_ecs_task_definition" "pretix_service" {
  family = "${terraform.workspace}-pretix"
  container_definitions = jsonencode([
    {
      name              = "pretix"
      image             = "${data.aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.image.image_digest}"
      memoryReservation = 1900
      essential         = true
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
          value = "redis://${aws_instance.redis.private_ip}/0"
        },
        {
          name  = "PRETIX_REDIS_SESSIONS",
          value = "false"
        },
        {
          name  = "PRETIX_CELERY_BROKER",
          value = "redis://${aws_instance.redis.private_ip}/1"
        },
        {
          name  = "PRETIX_CELERY_BACKEND",
          value = "redis://${aws_instance.redis.private_ip}/2"
        },
        {
          name  = "PRETIX_PRETIX_URL",
          value = "https://tickets.pycon.it/"
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
      ]
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
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
          "awslogs-group"         = aws_cloudwatch_log_group.pretix_logs.name
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

resource "aws_ecs_service" "pretix" {
  name                               = "${terraform.workspace}-pretix-service"
  cluster                            = aws_ecs_cluster.pretix.id
  task_definition                    = aws_ecs_task_definition.pretix_service.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
