resource "aws_security_group" "lambda" {
  vpc_id      = aws_vpc.default.id
  name        = "pythonit-lambda-security-group"
  description = "Lambda common security group"

  tags = {
    Name = "pythonit-lambda-security-group"
  }
}

resource "aws_security_group_rule" "allow_http" {
  type              = "egress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  security_group_id = aws_security_group.lambda.id
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "allow_https" {
  type              = "egress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  security_group_id = aws_security_group.lambda.id
  cidr_blocks       = ["0.0.0.0/0"]
}
