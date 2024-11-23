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
