resource "aws_db_subnet_group" "rds" {
  name        = "pythonit-rds-subnet"
  description = "Pythonit rds subnet"
  subnet_ids = [
    for subnet in aws_subnet.private :
    subnet.id
  ]

  tags = {
    Name = "pythonit-rds-subnet"
  }
}
