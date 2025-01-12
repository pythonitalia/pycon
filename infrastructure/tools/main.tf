terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = "5.82.2"
    }
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket = "xujw087uco-infrastructure-tools-opentofu"
    key    = "opentofu.tfstate"
    region = "eu-central-1"
  }
}

provider "aws" {
  region = "eu-central-1"
}

provider "github" {
  owner = "pythonitalia"
}
