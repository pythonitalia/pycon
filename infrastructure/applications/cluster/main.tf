resource "aws_ecs_cluster" "cluster" {
  name = "pythonit-${terraform.workspace}"
}

output "cluster_id" {
  value = aws_ecs_cluster.cluster.id
}

resource "aws_service_discovery_http_namespace" "cluster" {
  name        = "pythonit-${terraform.workspace}"
  description = "pythonit-${terraform.workspace} service discovery namespace"
}

output "service_connect_namespace" {
  value = aws_service_discovery_http_namespace.cluster.arn
}

resource "aws_ecs_account_setting_default" "trunking" {
  name  = "awsvpcTrunking"
  value = "enabled"
}
