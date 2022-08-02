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

resource "aws_instance" "pretix" {
  ami               = data.aws_ami.ecs.id
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

  tags = {
    Name = "${terraform.workspace}-pretix-instance"
  }
}

resource "aws_eip" "ip" {
  instance = aws_instance.pretix.id
  vpc      = true
  tags = {
    Name = "${terraform.workspace}-pretix"
  }
}

data "aws_db_proxy" "proxy" {
  count = var.enable_proxy ? 1 : 0
  name  = "pythonit-${terraform.workspace}-database-proxy"
}

resource "aws_ecs_task_definition" "pretix_service" {
  family = "${terraform.workspace}-pretix"
  container_definitions = jsonencode([
    {
      name      = "pretix"
      image     = "${data.aws_ecr_repository.repo.repository_url}@${data.aws_ecr_image.image.image_digest}"
      cpu       = 2048
      memory    = 1900
      essential = true
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
          value = "redis://${aws_elasticache_cluster.cache.cache_nodes.0.address}/0"
        },
        {
          name  = "PRETIX_REDIS_SESSIONS",
          value = "false"
        },
        {
          name  = "PRETIX_CELERY_BROKER",
          value = "redis://${aws_elasticache_cluster.cache.cache_nodes.0.address}/1"
        },
        {
          name  = "PRETIX_CELERY_BACKEND",
          value = "redis://${aws_elasticache_cluster.cache.cache_nodes.0.address}/2"
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
