resource "aws_security_group" "server" {
  name        = "pythonit-${terraform.workspace}-server"
  description = "pythonit-${terraform.workspace} server"
  vpc_id      = var.vpc_id

  tags = {
    Name = "pythonit-${terraform.workspace}-server"
  }
}

resource "aws_security_group_rule" "out_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "all"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.server.id
}

resource "aws_security_group_rule" "server_rds" {
  type              = "egress"
  from_port         = 5432
  to_port           = 5432
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.server.id
}

resource "aws_security_group_rule" "in_redis" {
  type              = "egress"
  from_port         = 6379
  to_port           = 6379
  protocol          = "tcp"
  source_security_group_id = aws_security_group.server.id
  security_group_id = aws_security_group.server.id
}

resource "aws_security_group_rule" "out_redis" {
  # needed by fargate to connect to the server with redis
  type              = "ingress"
  from_port         = 6379
  to_port           = 6379
  protocol          = "tcp"
  source_security_group_id = aws_security_group.server.id
  security_group_id = aws_security_group.server.id
}

resource "aws_security_group_rule" "in_clamav" {
  type              = "egress"
  from_port         = 3310
  to_port           = 3310
  protocol          = "tcp"
  source_security_group_id = aws_security_group.server.id
  security_group_id = aws_security_group.server.id
}

resource "aws_security_group_rule" "out_clamav" {
  # needed by fargate to connect to the server with clamav
  type              = "ingress"
  from_port         = 3310
  to_port           = 3310
  protocol          = "tcp"
  source_security_group_id = aws_security_group.server.id
  security_group_id = aws_security_group.server.id
}

resource "aws_security_group_rule" "web_http" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.server.id
}

resource "aws_security_group_rule" "server_ssh" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.server.id
}

output "security_group_id" {
  value = aws_security_group.server.id
}
