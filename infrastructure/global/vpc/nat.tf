resource "aws_eip" "nat_instance" {
  domain = "vpc"
  tags = {
    Name = "nat public ip"
  }
}

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

  ingress {
    description = "Clamav traffic"
    from_port   = 3310
    to_port     = 3310
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

  egress {
    from_port = 3310
    to_port =  3310
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "nat instance security group"
  }
}

data "template_file" "nat_user_data" {
  template = file("${path.module}/nat_instance_user_data.sh")
}

resource "aws_instance" "nat_instance" {
  ami                    = "ami-0c058ff13c7598bc3"
  instance_type          = "t4g.nano"
  availability_zone      = "eu-central-1a"
  subnet_id              = aws_subnet.public["eu-central-1a"].id
  vpc_security_group_ids = [aws_security_group.nat.id]
  source_dest_check      = false
  user_data              = data.template_file.nat_user_data.rendered
  key_name               = "pretix"

  root_block_device {
    volume_size = 8
  }

  tags = {
    Name = "nat instance"
  }
}

resource "aws_eip_association" "nat_instance_ip_assoc" {
  instance_id   = aws_instance.nat_instance.id
  allocation_id = aws_eip.nat_instance.id
}
