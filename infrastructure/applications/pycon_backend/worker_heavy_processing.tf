resource "aws_ecs_task_definition" "heavy_processing_worker" {
  family = "pythonit-${terraform.workspace}-heavy-processing-worker"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 4096
  memory                   = 16384
  network_mode             = "awsvpc"
  execution_role_arn = var.iam_role_arn
  task_role_arn = var.iam_role_arn

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

      command = [
        "/home/app/.venv/bin/celery", "-A", "pycon", "worker", "-l", "info", "-Q", "heavy_processing", "--hostname", "heavyprocessing@%h", "-E"
      ]

      environment = local.env_vars

      mountPoints = [
        {
          "containerPath" = "/tmp/"
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
          "awslogs-group"         = var.logs_group_name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "heavy-processing-worker"
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
