locals {
  is_prod       = terraform.workspace == "production"
}

# Applications

module "pretix" {
  source       = "./pretix"
  count        = 1
  server_ip = module.cluster.server_ip
  cluster_id = module.cluster.cluster_id
  logs_group_name = module.cluster.logs_group_name
  database_settings = module.database.database_settings
}

module "pycon_backend" {
  source       = "./pycon_backend"
  cluster_id = module.cluster.cluster_id
  security_group_id = module.cluster.security_group_id
  server_ip = module.cluster.server_ip
  logs_group_name = module.cluster.logs_group_name
  iam_role_arn = module.cluster.iam_role_arn
  database_settings = module.database.database_settings
  vpc_id = module.vpc.vpc_id
  public_1a_subnet_id = module.vpc.public_1a_subnet_id
  configuration_set_name = module.emails.configuration_set_name

  providers = {
    aws.us = aws.us
  }
}

module "pycon_frontend" {
  source       = "./pycon_frontend"
  cluster_id = module.cluster.cluster_id
  logs_group_name = module.cluster.logs_group_name
  server_ip = module.cluster.server_ip
  cf_domain_name = module.cluster.cf_domain_name
  cf_hosted_zone_id = module.cluster.cf_hosted_zone_id
}

module "clamav" {
  source       = "./clamav"
  cluster_id = module.cluster.cluster_id
  logs_group_name = module.cluster.logs_group_name
}

# Other resources

module "database" {
  source       = "./database"
  private_subnets_ids = module.vpc.private_subnets_ids
  vpc_id = module.vpc.vpc_id
}

module "emails" {
  source = "./emails"

  providers = {
    aws.us = aws.us
  }
}

module "cluster" {
  source = "./cluster"
  vpc_id = module.vpc.vpc_id
  public_1a_subnet_id = module.vpc.public_1a_subnet_id

  providers = {
    aws.us = aws.us
  }
}

module "vpc" {
  source = "./vpc"
}

output "server_public_ip" {
  value = module.cluster.server_public_ip
}
