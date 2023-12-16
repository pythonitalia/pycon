terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = "5.31.0"
      configuration_aliases = [aws.us]
    }
  }

  backend "s3" {
    bucket = "pycon-terraform"
    key    = "terraform.tfstate"
    region = "eu-central-1"
  }
}

provider "aws" {
  region = "eu-central-1"
}

provider "aws" {
  region = "us-east-1"
  alias  = "us"
}
