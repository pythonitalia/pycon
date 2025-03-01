resource "aws_security_group" "rds" {
  vpc_id      = var.vpc_id
  name        = "pythonit-${terraform.workspace}-rds-security-group"
  description = "Allow inbound postgres traffic"
}

resource "aws_security_group_rule" "allow_postgres" {
  type              = "ingress"
  from_port         = 5432
  to_port           = 5432
  protocol          = "tcp"
  security_group_id = aws_security_group.rds.id
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "allow_outbound_postgres" {
  type                     = "egress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.rds.id
  source_security_group_id = aws_security_group.rds.id
}
