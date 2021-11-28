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
  instance_type     = "t3.micro"
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

data "aws_ecr_repository" "repo" {
  name = "pythonit/pretix"
}

resource "aws_ecs_task_definition" "pretix_service" {
  family = "${terraform.workspace}-pretix"
  container_definitions = jsonencode([
    {
      name      = "pretix"
      image     = "${data.aws_ecr_repository.repo.repository_url}:latest"
      cpu       = 10
      memory    = 512
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
          name  = "SENTRY_DSN"
          value = module.secrets.value.sentry_dsn
        },
        {
          name  = "SECRET_KEY"
          value = module.secrets.value.secret_key
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
        }
      ]
    },
  ])

  volume {
    name      = "media"
    host_path = "/var/pretix/data/media"
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
