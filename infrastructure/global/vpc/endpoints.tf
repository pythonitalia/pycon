resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.default.id
  service_name      = "com.amazonaws.eu-central-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids = concat(
    [for route in aws_route_table.private : route.id],
    [for route in aws_route_table.public : route.id]
  )
}
