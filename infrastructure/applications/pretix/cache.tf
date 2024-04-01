resource "aws_elasticache_subnet_group" "default" {
  name        = "${terraform.workspace}-pretix-redis-subnet"
  description = "${terraform.workspace} pretix redis subnet"
  subnet_ids  = [for subnet in data.aws_subnets.private.ids : subnet]
}

resource "aws_elasticache_cluster" "cache" {
  cluster_id               = "${terraform.workspace}-pretix"
  engine                   = "redis"
  node_type                = "cache.t4g.micro"
  num_cache_nodes          = 1
  parameter_group_name     = "default.redis6.x"
  engine_version           = "6.2.5"
  port                     = 6379
  apply_immediately        = true
  snapshot_retention_limit = 0
  subnet_group_name        = aws_elasticache_subnet_group.default.name
  security_group_ids = [
    aws_security_group.instance.id
  ]

  lifecycle {
    ignore_changes = [engine_version]
  }
}

data "aws_ami" "ecs_arm" {
  most_recent = true

  filter {
    name   = "name"
    values = ["al2023-ami-ecs-hvm-2023.0.20240328-kernel-6.1-arm64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["arm64"]
  }

  owners = ["amazon"]
}
