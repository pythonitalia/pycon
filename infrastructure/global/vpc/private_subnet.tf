resource "aws_subnet" "private" {
  for_each          = local.private_azs_cidr
  vpc_id            = aws_vpc.default.id
  availability_zone = each.key
  cidr_block        = each.value

  tags = {
    Name = "private subnet ${each.key}"
    Type = "private"
  }
}

resource "aws_route_table" "private" {
  for_each = toset(keys(local.private_azs_cidr))
  vpc_id   = aws_vpc.default.id

  route {
    cidr_block  = "0.0.0.0/0"
    instance_id = aws_instance.nat[each.key].id
  }

  tags = {
    Name = "private subnet route table ${each.value}"
  }

  depends_on = [
    aws_instance.nat
  ]
}

resource "aws_route_table_association" "private_subnet_to_private_route" {
  for_each       = toset(keys(local.private_azs_cidr))
  route_table_id = aws_route_table.private[each.value].id
  subnet_id      = aws_subnet.private[each.value].id
}
