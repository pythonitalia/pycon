resource "aws_subnet" "public" {
  for_each                = local.public_azs_cidr
  vpc_id                  = aws_vpc.default.id
  availability_zone       = each.key
  cidr_block              = each.value
  map_public_ip_on_launch = true

  tags = {
    Name = "public subnet ${each.key}"
    Type = "public"
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
    Name = "public subnet route table ${each.value}"
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

# Internet gateway

resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id
}
