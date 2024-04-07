data "aws_ami" "ecs_arm" {
  most_recent = true

  filter {
    name   = "name"
    values = ["al2023-ami-ecs-hvm-2023.0.20240328-kernel-6.1-arm64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["arm64"]
  }

  owners = ["amazon"]
}

resource "aws_ecs_cluster" "redis" {
  name = "pythonit-${terraform.workspace}-redis"
}

data "template_file" "redis_data" {
  template = file("${path.module}/redis_userdata.sh")
  vars = {
    ecs_cluster = aws_ecs_cluster.redis.name
  }
}

resource "aws_ebs_volume" "redis_data" {
  availability_zone = "eu-central-1a"
  size              = 10
  type              = "gp3"

  tags = {
    Name = "redis-data"
  }
}

resource "aws_volume_attachment" "redis_data_attachment" {
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.redis_data.id
  instance_id = aws_instance.redis.id
}

resource "aws_instance" "redis" {
  ami               = data.aws_ami.ecs_arm.id
  instance_type     = "t4g.nano"
  subnet_id         = data.aws_subnet.private.id
  availability_zone = "eu-central-1a"
  vpc_security_group_ids = [
    aws_security_group.instance.id
  ]
  source_dest_check    = true
  user_data            = data.template_file.redis_data.rendered
  iam_instance_profile = aws_iam_instance_profile.instance.name
  key_name             = "pretix"

  root_block_device {
    volume_size = 30
  }

  tags = {
    Name = "pythonit-${terraform.workspace}-redis"
  }
}

resource "aws_cloudwatch_log_group" "redis_logs" {
  name              = "/ecs/pythonit-${terraform.workspace}-redis"
  retention_in_days = 3
}

resource "aws_ecs_task_definition" "redis" {
  family = "pythonit-${terraform.workspace}-redis"
  container_definitions = jsonencode([
    {
      name              = "redis"
      image             = "redis:6.2.6"
      memoryReservation = 400
      essential         = true
      portMappings = [
        {
          containerPort = 6379
          hostPort      = 6379
        }
      ]

      mountPoints    = [
        {
          sourceVolume = "redis-data"
          containerPath = "/data"
          readOnly = false
        }
      ]
      systemControls = []

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.redis_logs.name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }

      healthCheck = {
        retries = 3
        command = [
          "CMD-SHELL",
          "redis-cli ping"
        ]
        timeout  = 3
        interval = 10
      }

      stopTimeout = 300
    }
  ])

  volume {
    name      = "redis-data"
    host_path = "/redis-data"
  }

  requires_compatibilities = []
  tags                     = {}
}

resource "aws_ecs_service" "redis" {
  name                               = "pythonit-${terraform.workspace}-redis"
  cluster                            = aws_ecs_cluster.redis.id
  task_definition                    = aws_ecs_task_definition.redis.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
