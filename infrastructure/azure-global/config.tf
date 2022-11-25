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
