terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.29.0"
    }
  }

  backend "s3" {
    bucket               = "pycon-terraform"
    key                  = "global-terraform/global_terraform.tfstate"
    workspace_key_prefix = "global-terraform"
    region               = "eu-central-1"
  }
}

provider "aws" {
  region = "eu-central-1"
}

provider "aws" {
  region = "us-east-1"
  alias  = "us"
}
