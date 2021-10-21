locals {
  normalized_workspace = replace(terraform.workspace, "-", "")
  is_prod              = terraform.workspace == "production"
}

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
  identifier                  = "pythonit-${terraform.workspace}"
  allow_major_version_upgrade = true
  engine_version              = "11.12"
  instance_class              = "db.t2.micro"
  name                        = "${local.normalized_workspace}backend"
  username                    = "root"
  password                    = module.common_secrets.value.database_password
  multi_az                    = "false"
  availability_zone           = "eu-central-1a"
  skip_final_snapshot         = true
  publicly_accessible         = false
  apply_immediately           = true
  backup_retention_period     = local.is_prod ? 7 : 0

  db_subnet_group_name   = data.aws_db_subnet_group.rds.name
  vpc_security_group_ids = [data.aws_security_group.rds.id]
}
