terraform {
    backend "s3" {
      bucket = "pycon-terraform"
      key    = "terraform.tfstate"
      region = "eu-central-1"
    }
}

provider "aws" {
  region = "eu-central-1"
}

data "aws_caller_identity" "current" {}
