resource "aws_security_group" "instance" {
  name        = "pythonit-${terraform.workspace}-worker-instance"
  description = "pythonit-${terraform.workspace} worker instance"
  vpc_id      = data.aws_vpc.default.id
}

resource "aws_security_group_rule" "ssh" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.instance.id
}
