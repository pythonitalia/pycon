terraform {
  backend "s3" {
    bucket = "pycon-terraform"
    key    = "terraform.tfstate"
    region = "eu-central-1"
  }
}

provider "aws" {
  region  = "eu-central-1"
  version = "3.21"
}

data "aws_caller_identity" "current" {}

# test change to trigger CI
