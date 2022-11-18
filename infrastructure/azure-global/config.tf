terraform {
  cloud {
    organization = "python-italia"

    workspaces {
      name = "global-infrastructure-azure"
    }
  }
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.31.0"
    }
  }
}

provider "azurerm" {
  features {}
}
