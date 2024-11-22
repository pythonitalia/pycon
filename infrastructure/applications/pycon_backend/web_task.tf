resource "aws_ecs_task_definition" "web" {
  family = "pythonit-${terraform.workspace}-web"

  container_definitions = jsonencode([
    {
      name              = "web"
      image             = "${data.aws_ecr_repository.be_repo.repository_url}@${data.aws_ecr_image.be_arm_image.image_digest}"
      memoryReservation = 200
      essential         = true
      entrypoint = [
        "/home/app/.venv/bin/gunicorn",
      ]

      command = [
        "-w", "4", "pycon.wsgi"
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

resource "aws_ecs_service" "backend" {
  name                               = "backend-web"
  cluster                            = var.cluster_id
  task_definition                    = aws_ecs_task_definition.web.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200
}
