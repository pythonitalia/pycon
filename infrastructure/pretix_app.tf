resource "aws_elastic_beanstalk_application" "pretix" {
  name        = "pretix"
  description = "pretix"
}

resource "aws_elastic_beanstalk_environment" "pretix_env" {
  name                = "${terraform.workspace}-pretix"
  application         = "${aws_elastic_beanstalk_application.pretix.name}"
  solution_stack_name = "64bit Amazon Linux 2018.03 v2.12.16 running Docker 18.06.1-ce"
  tier                = "WebServer"

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = "${aws_vpc.default.id}"
  }

  # This is the subnet of the ELB
  setting {
    namespace = "aws:ec2:vpc"
    name      = "ELBSubnets"
    value     = "${aws_subnet.primary.id}"
  }

  # This is the subnets for the instances.
  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = "${aws_subnet.primary.id}"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = "${aws_security_group.backend_rds.id}"
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
    value     = "${aws_iam_instance_profile.pycon.name}"
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
    value     = "${aws_db_instance.backend.username}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DATABASE_PASSWORD"
    value     = "${aws_db_instance.backend.password}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DATABASE_HOST"
    value     = "${aws_db_instance.backend.address}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "MAIL_USER"
    value     = "${var.mail_user}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "MAIL_PASSWORD"
    value     = "${var.mail_password}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SENTRY_DSN"
    value     = "${var.sentry_dsn}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SECRET_KEY"
    value     = "${var.pretix_secret_key}"
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
}

output "pretix_domain" {
  value = "${aws_elastic_beanstalk_environment.pretix_env.cname}"
}
