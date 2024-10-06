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
  count        = local.deploy_pretix ? 1 : 0
  ecs_arm_ami  = local.ecs_arm_ami
}

module "pycon_backend" {
  source       = "./pycon_backend"
  ecs_arm_ami  = local.ecs_arm_ami

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
