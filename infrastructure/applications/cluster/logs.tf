resource "aws_cloudwatch_log_group" "cluster" {
  name              = "/ecs/pythonit-${terraform.workspace}-cluster"
  retention_in_days = 3
}
