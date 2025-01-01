resource "aws_db_subnet_group" "rds" {
  name = "pythonit-${terraform.workspace}-rds-subnet"
  description = "Pythonit rds subnet"
  subnet_ids = var.private_subnets_ids

  tags = {
    Name = "pythonit-${terraform.workspace}-rds-subnet"
  }
}
