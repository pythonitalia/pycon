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
  ami               = var.ecs_x86_ami
  instance_type     = "t3.small"
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
          value = var.enable_proxy ? data.aws_db_proxy.proxy[0].endpoint : data.aws_db_instance.database.address
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
        }
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
