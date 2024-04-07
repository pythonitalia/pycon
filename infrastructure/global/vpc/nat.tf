resource "aws_security_group" "nat" {
  name        = "nat-instance-security-group"
  description = "Allow NAT traffic"
  vpc_id      = aws_vpc.default.id

  ingress {
    description = "HTTP traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.default.cidr_block]
  }

  ingress {
    description = "HTTPs traffic"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.default.cidr_block]
  }

  ingress {
    description = "Postgres traffic"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.default.cidr_block]
  }

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "nat instance security group"
  }
}

data "aws_instance" "nat_instance" {
  instance_tags = {
    Name = "production-pretix-instance"
  }
  filter {
    name   = "instance-state-name"
    values = ["running"]
  }
}
