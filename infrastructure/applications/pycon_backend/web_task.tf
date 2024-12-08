resource "aws_ecs_task_definition" "web" {
  family = "pythonit-${terraform.workspace}-web"

  container_definitions = jsonencode([
    {
      name              = "web"
      image             = "${data.aws_ecr_repository.be_repo.repository_url}@${data.aws_ecr_image.be_arm_image.image_digest}"
      memoryReservation = local.is_prod ? 400 : 10
      essential         = true
      entrypoint = [
        "/home/app/.venv/bin/gunicorn",
      ]

      command = [
        "-w", "5", "-b", "0.0.0.0:8000", "pycon.wsgi"
      ]

      dockerLabels = {
        "traefik.enable"                        = "true"
        "traefik.http.routers.backend-web.rule" = "PathPrefix(`/`)"
        "traefik.http.services.backend-web.loadbalancer.healthcheck.path" = "/health/"
        "traefik.http.services.backend-web.loadbalancer.healthcheck.interval" = "5s"
        "traefik.http.services.backend-web.loadbalancer.healthcheck.timeout" = "3s"
        "traefik.http.services.backend-web.loadbalancer.server.drain.duration" = "15s"
      }
      environment = local.env_vars

      portMappings = [
        {
          containerPort = 8000
          hostPort      = 0
        },
      ]

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
          "awslogs-group"         = var.logs_group_name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "backend-web"
        }
      }

      healthCheck = {
        retries = 3
        command = [
          "CMD-SHELL",
          "curl -f http://127.0.0.1:8000/health/ || exit 1"
        ]
        timeout  = 3
        interval = 10
      }

      stopTimeout = 35
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
