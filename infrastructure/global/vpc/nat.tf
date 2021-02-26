data "aws_ami" "nat" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn-ami-vpc-nat-2018.03.0.20190826-x86_64-ebs"]
  }

  owners = ["137112412989"] # Amazon
}

resource "aws_eip" "nat" {
  for_each = toset(keys(local.public_azs_cidr))
  vpc      = true
  tags = {
    Name = "nat public ip ${each.key}"
  }
}

resource "aws_eip_association" "nat_ip_assoc" {
  for_each      = toset(keys(local.public_azs_cidr))
  instance_id   = aws_instance.nat[each.key].id
  allocation_id = aws_eip.nat[each.key].id
}

resource "aws_instance" "nat" {
  for_each               = toset(keys(local.public_azs_cidr))
  ami                    = data.aws_ami.nat.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public[each.key].id
  availability_zone      = each.key
  vpc_security_group_ids = [aws_security_group.nat.id]
  source_dest_check      = false

  tags = {
    Name = "nat instance - ${each.key}"
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

  tags = {
    Name = "nat instance security group"
  }
}
