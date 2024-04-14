locals {
  is_prod       = terraform.workspace == "production"
  deploy_pretix = local.is_prod
  enable_proxy  = local.is_prod ? false : false

  # AMI
  # Built from https://github.com/aws/amazon-ecs-ami
  # Using 8GB as storage.
  ecs_x86_ami = "ami-081185af466969baa" # make al2023
  ecs_arm_ami = "ami-08d9c5f7f3465a286" # make al2023arm
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
