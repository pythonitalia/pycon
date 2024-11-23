resource "aws_subnet" "private" {
  for_each          = local.private_azs_cidr
  vpc_id            = aws_vpc.default.id
  availability_zone = each.key
  cidr_block        = each.value

  tags = {
    Name = "private subnet ${each.key}"
    Type = "private"
    AZ   = each.key
  }
}

resource "aws_route_table_association" "private_subnet_to_private_route" {
  for_each       = toset(keys(local.private_azs_cidr))
  route_table_id = aws_route_table.private[each.value].id
  subnet_id      = aws_subnet.private[each.value].id
}
