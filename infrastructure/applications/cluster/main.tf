locals {
  is_prod = terraform.workspace == "production"
}

resource "aws_ecs_cluster" "cluster" {
  name = "pythonit-${terraform.workspace}"
}

output "cluster_id" {
  value = aws_ecs_cluster.cluster.id
}

resource "aws_ecs_account_setting_default" "trunking" {
  name  = "awsvpcTrunking"
  value = "enabled"
}
