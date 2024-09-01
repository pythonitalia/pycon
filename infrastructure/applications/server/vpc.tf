data "aws_vpc" "default" {
  filter {
    name   = "tag:Name"
    values = ["pythonit-vpc"]
  }
}

data "aws_subnet" "public_1a" {
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
