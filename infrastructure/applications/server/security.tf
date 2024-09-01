data "aws_security_group" "lambda" {
  name = "pythonit-lambda-security-group"
}

data "aws_security_group" "rds" {
  name = "pythonit-rds-security-group"
}

resource "aws_security_group" "server" {
  name        = "${terraform.workspace}-server"
  description = "${terraform.workspace} server"
  vpc_id      = data.aws_vpc.default.id
}

resource "aws_security_group_rule" "out_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "all"
  cidr_blocks       = ["0.0.0.0/0"]
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

resource "aws_security_group_rule" "web_dashboard" {
  type              = "ingress"
  from_port         = 8080
  to_port           = 8080
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.server.id
}
