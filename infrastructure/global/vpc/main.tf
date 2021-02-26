locals {
  public_azs_cidr = {
    "eu-central-1a" : "10.0.1.0/24",
    "eu-central-1b" : "10.0.2.0/24"
  }
  private_azs_cidr = {
    "eu-central-1a" : "10.0.4.0/24",
    "eu-central-1b" : "10.0.5.0/24"
  }
}

resource "aws_vpc" "default" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "pythonit-vpc"
  }
}
