resource "aws_security_group" "backend_rds" {
  vpc_id      = "${aws_vpc.default.id}"
  name        = "${terraform.workspace}_backend_rds"
  description = "Allow inbound postgres traffic"
}

resource "aws_security_group_rule" "allow_postgres" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = "${aws_security_group.backend_rds.id}"
  source_security_group_id = "${aws_security_group.backend_rds.id}"
}

resource "aws_db_subnet_group" "backend_rds" {
  name       = "${terraform.workspace}_backend_rds"
  subnet_ids = ["${aws_subnet.primary.id}", "${aws_subnet.secondary.id}"]
}


resource "aws_db_instance" "backend" {
  allocated_storage   = 10
  storage_type        = "gp2"
  engine              = "postgres"
  engine_version      = "9.6.11"
  instance_class      = "db.t2.micro"
  name                = "${terraform.workspace}backend"
  username            = "root"
  password            = "${var.database_password}"
  multi_az            = "false"
  availability_zone   = "eu-central-1a"
  skip_final_snapshot = true

  db_subnet_group_name   = "${aws_db_subnet_group.backend_rds.name}"
  vpc_security_group_ids = ["${aws_security_group.backend_rds.id}"]
}
