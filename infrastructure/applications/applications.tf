locals {
  is_prod       = terraform.workspace == "production"
  deploy_pretix = local.is_prod
  enable_proxy  = local.is_prod ? false : false

  # AMI
  # Built from https://github.com/aws/amazon-ecs-ami
  # Using 8GB as storage.
  ecs_x86_ami = "ami-04467750a630d1f7c" # make al2023
  ecs_arm_ami = "ami-0bd650c1ca04cc1a4" # make al2023arm
}

# Applications

module "pretix" {
  source       = "./pretix"
  count        = local.deploy_pretix ? 1 : 0
  enable_proxy = local.enable_proxy
  ecs_x86_ami  = local.ecs_x86_ami
  ecs_arm_ami  = local.ecs_arm_ami
}

module "pycon_backend" {
  source       = "./pycon_backend"
  enable_proxy = local.enable_proxy
  ecs_arm_ami  = local.ecs_arm_ami

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "email_templates" {
  source = "./email_templates"
}

# Other resources

module "database" {
  source       = "./database"
  enable_proxy = local.enable_proxy
}

module "emails" {
  source = "./emails"

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "server" {
  source      = "./server"
  ecs_arm_ami = local.ecs_arm_ami

  providers = {
    aws    = aws
    aws.us = aws.us
  }
}

module "pretix_arm" {
  source = "./pretix_arm"
  ecs_arm_ami = local.ecs_arm_ami
}
