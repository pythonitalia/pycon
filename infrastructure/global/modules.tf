# Generic
module "ecr_repos" {
  source = "./ecr_repos"
}

# Domains

module "python_it" {
  source = "./domains/python_it"
}

module "pycon_it" {
  source = "./domains/pycon_it"
}

# VPC

module "vpc" {
  source = "./vpc"
}

# Roles

module "iam_roles" {
  source = "./iam_roles"
}

# Certs

module "certs_beta" {
  source = "./certs/beta"

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}
