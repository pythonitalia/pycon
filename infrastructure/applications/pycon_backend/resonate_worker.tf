resource "aws_ecs_task_definition" "resonate_worker" {
  family = "pythonit-${terraform.workspace}-resonate-worker"

  container_definitions = jsonencode([
    {
      name              = "resonate-worker"
      image             = "${data.aws_ecr_repository.be_repo.repository_url}@${data.aws_ecr_image.be_arm_image.image_digest}"
      memoryReservation = local.is_prod ? 200 : 10
      essential         = true

      # Reloading is off outside DEBUG anyway; saying so keeps the deployed
      # process a single one, with no reloader parent to sit between ECS and
      # the worker's own signal handling.
      command = [
        "python", "manage.py", "resonate_worker", "--no-reload"
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
          "awslogs-group"         = var.logs_group_name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "resonate-worker"
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

      # Long enough for the worker to hand its tasks back to the server
      # instead of letting their leases lapse.
      stopTimeout = 120
    }
  ])

  requires_compatibilities = []
  tags                     = {}
}

resource "aws_ecs_service" "resonate_worker" {
  name                               = "backend-resonate-worker"
  cluster                            = var.cluster_id
  task_definition                    = aws_ecs_task_definition.resonate_worker.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
