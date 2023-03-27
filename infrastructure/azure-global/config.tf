terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.34.0"
    }
    azapi = {
      source  = "azure/azapi"
      version = "~>0.4.0"
    }
    acme = {
      source  = "vancluever/acme"
      version = "~> 2.13.1"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  cloud {
    organization = "python-italia"

    workspaces {
      name = "global-infrastructure-azure"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "azapi" {}

provider "acme" {
  server_url = "https://acme-v02.api.letsencrypt.org/directory"
}

provider "aws" {
  region = "eu-central-1"
}
