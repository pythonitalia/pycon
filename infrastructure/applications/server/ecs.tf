resource "aws_ecs_cluster" "server" {
  name = "${terraform.workspace}-server"
}
