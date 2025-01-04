resource "aws_ecs_cluster" "github_runners" {
  name = "github-actions-runners"
}

resource "aws_ecs_cluster_capacity_providers" "github_runners" {
  cluster_name = aws_ecs_cluster.github_runners.name

  capacity_providers = ["FARGATE_SPOT"]

  default_capacity_provider_strategy {
    base              = 1
    weight            = 100
    capacity_provider = "FARGATE_SPOT"
  }
}
