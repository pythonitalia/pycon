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
