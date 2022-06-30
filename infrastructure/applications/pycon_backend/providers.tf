terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.61.0"
      configuration_aliases = [aws.us]
    }
  }
}
