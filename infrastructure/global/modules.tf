module "ecr_repos" {
  source = "./ecr_repos"
}

module "python_it" {
  source = "./domains/python_it"
}

module "pycon_it" {
  source = "./domains/pycon_it"
}

module "pydata_it" {
  source = "./domains/pydata_it"
}

module "certs_beta" {
  source = "./certs/beta"

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "certs" {
  source = "./certs"

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "buckets" {
  source = "./buckets"
}

module "archives" {
  source = "./archives"

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "ses" {
  source = "./ses"
}
