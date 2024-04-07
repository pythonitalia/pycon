resource "aws_security_group" "instance" {
  name        = "${terraform.workspace}-pretix-instance"
  description = "${terraform.workspace} pretix instance"
  vpc_id      = data.aws_vpc.default.id
}

resource "aws_security_group_rule" "out_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "all"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.instance.id
}

resource "aws_security_group_rule" "web_http" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.instance.id
}

resource "aws_security_group_rule" "allow_redis" {
  type                     = "ingress"
  from_port                = 6379
  to_port                  = 6379
  protocol                 = "tcp"
  security_group_id        = aws_security_group.instance.id
  source_security_group_id = aws_security_group.instance.id
}

data "aws_security_group" "lambda" {
  name = "pythonit-lambda-security-group"
}

resource "aws_security_group_rule" "allow_redis_from_lambda" {
  type                     = "ingress"
  from_port                = 6379
  to_port                  = 6379
  protocol                 = "tcp"
  security_group_id        = aws_security_group.instance.id
  source_security_group_id = data.aws_security_group.lambda.id
}
