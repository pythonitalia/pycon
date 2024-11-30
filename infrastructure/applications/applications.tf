locals {
  is_prod       = terraform.workspace == "production"
  deploy_pretix = local.is_prod

  # AMI
  # Built from https://github.com/aws/amazon-ecs-ami
  # Using 8GB as storage.
  ecs_arm_ami = "ami-0bd650c1ca04cc1a4" # make al2023arm
}

# Applications

module "pretix" {
  source       = "./pretix"
  count        = 1
  ecs_arm_ami  = local.ecs_arm_ami
  server_ip = module.cluster.server_ip
  cluster_id = module.cluster.cluster_id
  logs_group_name = module.cluster.logs_group_name
}

module "pycon_backend" {
  source       = "./pycon_backend"
  ecs_arm_ami  = local.ecs_arm_ami
  cluster_id = module.cluster.cluster_id
  security_group_id = module.cluster.security_group_id
  server_ip = module.cluster.server_ip
  logs_group_name = module.cluster.logs_group_name
  iam_role_arn = module.cluster.iam_role_arn

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "clamav" {
  source       = "./clamav"
  cluster_id = module.cluster.cluster_id
  logs_group_name = module.cluster.logs_group_name

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

# Other resources

module "database" {
  source       = "./database"
}

module "emails" {
  source = "./emails"

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "cluster" {
  source = "./cluster"
  ecs_arm_ami  = local.ecs_arm_ami

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

output "server_public_ip" {
  value = module.cluster.server_public_ip
}
