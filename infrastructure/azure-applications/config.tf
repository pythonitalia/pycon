locals {
  workspace           = replace(terraform.workspace, "applications-", "")
  is_prod             = local.workspace == "production"
  resource_group_name = "pythonitalia-${local.workspace}"
}

terraform {
  cloud {
    organization = "python-italia"

    workspaces {
      tags = ["applications"]
    }
  }

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
