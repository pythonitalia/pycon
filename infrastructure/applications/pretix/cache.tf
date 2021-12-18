resource "aws_elasticache_subnet_group" "default" {
  name        = "${terraform.workspace}-pretix-redis-subnet"
  description = "${terraform.workspace} pretix redis subnet"
  subnet_ids  = [for subnet in data.aws_subnet_ids.private.ids : subnet]
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
}
