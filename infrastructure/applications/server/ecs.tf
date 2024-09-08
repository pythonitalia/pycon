resource "aws_ecs_cluster" "server" {
  name = "${terraform.workspace}-server"
}

resource "aws_ecs_capacity_provider" "server" {
  name = "pythonit-${terraform.workspace}-server"

  auto_scaling_group_provider {
    auto_scaling_group_arn         = aws_autoscaling_group.server.arn
    managed_termination_protection = "ENABLED"

    managed_scaling {
      maximum_scaling_step_size = 2
      minimum_scaling_step_size = 1
      status                    = "ENABLED"
      target_capacity           = 1
      instance_warmup_period    = 60
    }
  }
}

resource "aws_ecs_cluster_capacity_providers" "server" {
  cluster_name = aws_ecs_cluster.server.name
  capacity_providers = [
    aws_ecs_capacity_provider.server.name,
  ]

  default_capacity_provider_strategy {
    base              = 1
    weight            = 100
    capacity_provider = aws_ecs_capacity_provider.server.name
  }
}
