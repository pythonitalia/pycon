resource "aws_ecs_cluster" "heavy_processing_worker" {
  name = "pythonit-${terraform.workspace}-heavy-processing-worker"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_cloudwatch_log_group" "heavy_processing_worker_logs" {
  name              = "/ecs/pythonit-${terraform.workspace}-heavy-processing-worker"
  retention_in_days = 7
}

resource "aws_ecs_task_definition" "heavy_processing_worker" {
  family = "pythonit-${terraform.workspace}-heavy-processing-worker"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 4096
  memory                   = 16384
  network_mode             = "awsvpc"
  execution_role_arn = aws_iam_role.worker.arn
  task_role_arn = aws_iam_role.worker.arn

  ephemeral_storage {
    size_in_gib = 21
  }
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture = "ARM64"
  }
  container_definitions = jsonencode([
    {
      name              = "worker"
      image             = "${data.aws_ecr_repository.be_repo.repository_url}@${data.aws_ecr_image.be_arm_image.image_digest}"
      memoryReservation = 16384
      essential         = true
      entrypoint = [
        "/home/app/.venv/bin/celery",
      ]

      command = [
        "-A", "pycon", "worker", "-c", "2", "-l", "info", "-Q", "heavy_processing", "--hostname", "heavyprocessing@%h", "-E"
      ]

      environment = local.env_vars

      mountPoints = [
        {
          "containerPath" = "/tmp"
          "sourceVolume"  = "storage"
          "readOnly"      = false
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
          "awslogs-group"         = aws_cloudwatch_log_group.heavy_processing_worker_logs.name
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

      stopTimeout = 120
    }
  ])

  volume {
    name = "storage"
    configure_at_launch = true
  }

  tags                     = {}
}
