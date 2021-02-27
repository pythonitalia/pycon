resource "aws_elastic_beanstalk_application" "app" {
  name        = "pretix"
  description = "pretix"
}

data "aws_db_instance" "database" {
  db_instance_identifier = "terraform-20190815202105324300000001"
}

resource "aws_elastic_beanstalk_environment" "env" {
  name                = "${terraform.workspace}-pretix"
  application         = aws_elastic_beanstalk_application.app.name
  solution_stack_name = "64bit Amazon Linux 2018.03 v2.12.16 running Docker 18.06.1-ce"
  tier                = "WebServer"

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = "vpc-0abcff21ccd9b860d"
  }

  # This is the subnet of the ELB
  setting {
    namespace = "aws:ec2:vpc"
    name      = "ELBSubnets"
    value     = "subnet-0ac523ae11fd2a78e"
  }

  # This is the subnets for the instances.
  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = "subnet-0ac523ae11fd2a78e"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = "sg-03023e3f90c685344"
  }

  # You can set the environment type, single or LoadBalanced
  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "SingleInstance"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "ng-beanstalk-ec2-user-production"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DATABASE_NAME"
    # TODO make database name dynamic
    value = "pretix"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DATABASE_USERNAME"
    value     = data.aws_db_instance.database.master_username
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DATABASE_PASSWORD"
    value     = var.database_password
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DATABASE_HOST"
    value     = data.aws_db_instance.database.address
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "MAIL_USER"
    value     = var.mail_user
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "MAIL_PASSWORD"
    value     = var.mail_password
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SENTRY_DSN"
    value     = var.sentry_dsn
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SECRET_KEY"
    value     = var.secret_key
  }

  # Are the load balancers multizone?
  setting {
    namespace = "aws:elb:loadbalancer"
    name      = "CrossZone"
    value     = "true"
  }

  # Enable connection draining.
  setting {
    namespace = "aws:elb:policies"
    name      = "ConnectionDrainingEnabled"
    value     = "true"
  }

  lifecycle {
    # Temporary because EB thinks settings are always different
    ignore_changes = [setting]
  }
}

output "pretix_domain" {
  value = aws_elastic_beanstalk_environment.env.cname
}
