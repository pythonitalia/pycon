data "aws_db_instance" "database" {
  db_instance_identifier = "pythonit-${terraform.workspace}"
}
