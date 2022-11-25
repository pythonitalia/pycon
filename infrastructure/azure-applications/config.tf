locals {
  workspace               = replace(terraform.workspace, "applications-", "")
  is_prod                 = local.workspace == "production"
  resource_group_name     = "pythonitalia-${local.workspace}"
  resource_group_location = "germanywestcentral"
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
      version = "=3.47.0"
    }
    azapi = {
      source  = "azure/azapi"
      version = "~>0.4.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}

provider "azapi" {}
