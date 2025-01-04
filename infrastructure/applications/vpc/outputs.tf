output "private_subnets_ids" {
  value = [for subnet in aws_subnet.private : subnet.id]
}

output "vpc_id" {
  value = aws_vpc.default.id
}

output "public_1a_subnet_id" {
  value = aws_subnet.public["eu-central-1a"].id
}
