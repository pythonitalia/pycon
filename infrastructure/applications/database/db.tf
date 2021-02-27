data "aws_vpc" "default" {
  id = "vpc-0abcff21ccd9b860d"
}

resource "aws_security_group" "rds" {
  vpc_id      = data.aws_vpc.default.id
  name        = "${terraform.workspace}_backend_rds"
  description = "Allow inbound postgres traffic"
}

resource "aws_security_group_rule" "allow_postgres" {
  type              = "ingress"
  from_port         = 5432
  to_port           = 5432
  protocol          = "tcp"
  security_group_id = aws_security_group.rds.id
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "allow_outbound_postgres" {
  type                     = "egress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.rds.id
  source_security_group_id = aws_security_group.rds.id
}

data "aws_subnet_ids" "subnets" {
  vpc_id = data.aws_vpc.default.id
}

resource "aws_db_subnet_group" "rds" {
  name       = "${terraform.workspace}_backend_rds"
  subnet_ids = data.aws_subnet_ids.subnets.ids
}

# New
data "aws_db_subnet_group" "rds" {
  name = "pythonit-rds-subnet"
}

data "aws_security_group" "rds" {
  name = "pythonit-rds-security-group"
}

resource "aws_db_instance" "database" {
  allocated_storage           = 10
  storage_type                = "gp2"
  engine                      = "postgres"
  allow_major_version_upgrade = true
  engine_version              = "11.8"
  instance_class              = "db.t2.micro"
  name                        = "${terraform.workspace}backend"
  username                    = "root"
  password                    = var.database_password
  multi_az                    = "false"
  availability_zone           = "eu-central-1a"
  skip_final_snapshot         = true
  publicly_accessible         = false
  apply_immediately           = true
  backup_retention_period     = 7

  db_subnet_group_name   = data.aws_db_subnet_group.rds.name
  vpc_security_group_ids = [data.aws_security_group.rds.id]
}
