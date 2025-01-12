locals {
  public_azs_cidr = {
    "eu-central-1a" : "10.0.1.0/24",
    "eu-central-1b" : "10.0.2.0/24",
    "eu-central-1c" : "10.0.3.0/24",
  }
  private_azs_cidr = {
    "eu-central-1a" : "10.0.4.0/24",
    "eu-central-1b" : "10.0.5.0/24",
    "eu-central-1c" : "10.0.6.0/24",
  }
}

resource "aws_vpc" "default" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "private" {
  for_each          = local.private_azs_cidr
  vpc_id            = aws_vpc.default.id
  availability_zone = each.key
  cidr_block        = each.value

  tags = {
    Name = "main-vpc-private-subnet-${each.key}"
    Type = "private"
    AZ   = each.key
  }
}

resource "aws_subnet" "public" {
  for_each                = local.public_azs_cidr
  vpc_id                  = aws_vpc.default.id
  availability_zone       = each.key
  cidr_block              = each.value
  map_public_ip_on_launch = true

  tags = {
    Name = "main-vpc-public-subnet-${each.key}"
    Type = "public"
    AZ   = each.key
  }
}

resource "aws_route_table" "public" {
  for_each = toset(keys(local.public_azs_cidr))
  vpc_id   = aws_vpc.default.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }

  tags = {
    Name = "main-vpc-public-route-${each.value}"
  }

  depends_on = [
    aws_internet_gateway.default
  ]
}

resource "aws_route_table_association" "public_subnet_to_public_route" {
  for_each       = toset(keys(local.public_azs_cidr))
  route_table_id = aws_route_table.public[each.value].id
  subnet_id      = aws_subnet.public[each.value].id
}

resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id
}
