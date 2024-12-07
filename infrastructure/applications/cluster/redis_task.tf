resource "aws_ecs_task_definition" "redis" {
  family = "pythonit-${terraform.workspace}-redis"

  container_definitions = jsonencode([
    {
      name              = "redis"
      image             = "redis:6.2.6"
      memoryReservation = local.is_prod ? 400 : 10
      essential         = true
      portMappings = [
        {
          containerPort = 6379
          hostPort      = 6379
          name = "redis"
        }
      ]

      mountPoints = [
        {
          sourceVolume  = "redis-data"
          containerPath = "/data"
          readOnly      = false
        }
      ]
      systemControls = []

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.cluster.name
          "awslogs-region"        = "eu-central-1"
          "awslogs-stream-prefix" = "redis"
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
  name                               = "redis"
  cluster                            = aws_ecs_cluster.cluster.id
  task_definition                    = aws_ecs_task_definition.redis.arn
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100
}
