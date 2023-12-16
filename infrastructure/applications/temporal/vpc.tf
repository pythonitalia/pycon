data "aws_vpc" "default" {
  filter {
    name   = "tag:Name"
    values = ["pythonit-vpc"]
  }
}

data "aws_security_group" "rds" {
  name = "pythonit-rds-security-group"
}

data "aws_subnet" "private" {
  vpc_id = data.aws_vpc.default.id

  filter {
    name   = "tag:Type"
    values = ["private"]
  }

  filter {
    name   = "tag:AZ"
    values = ["eu-central-1a"]
  }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }

  tags = {
    Type = "private"
  }
}
