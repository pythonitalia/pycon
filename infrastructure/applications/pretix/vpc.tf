data "aws_vpc" "default" {
  filter {
    name   = "tag:Name"
    values = ["pythonit-vpc"]
  }
}

data "aws_security_group" "rds" {
  name = "pythonit-rds-security-group"
}

data "aws_subnet" "public" {
  vpc_id = data.aws_vpc.default.id

  filter {
    name   = "tag:Type"
    values = ["public"]
  }

  filter {
    name   = "tag:AZ"
    values = ["eu-central-1a"]
  }
}
