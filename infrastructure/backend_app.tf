resource "aws_elastic_beanstalk_application" "pycon" {
  name        = "pycon"
  description = "pycon"
}

resource "aws_elastic_beanstalk_environment" "pycon_env" {
  name                = "${terraform.workspace}-env"
  application         = aws_elastic_beanstalk_application.pycon.name
  solution_stack_name = "64bit Amazon Linux 2018.03 v2.12.16 running Docker 18.06.1-ce"
  tier                = "WebServer"

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = aws_vpc.default.id
  }

  # This is the subnet of the ELB
  setting {
    namespace = "aws:ec2:vpc"
    name      = "ELBSubnets"
    value     = aws_subnet.primary.id
  }

  # This is the subnets for the instances.
  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = aws_subnet.primary.id
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = aws_security_group.backend_rds.id
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
    value     = aws_iam_instance_profile.pycon.name
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DATABASE_URL"
    value     = "postgres://${aws_db_instance.backend.username}:${aws_db_instance.backend.password}@${aws_db_instance.backend.address}:${aws_db_instance.backend.port}/${aws_db_instance.backend.name}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SECRET_KEY"
    value     = var.secret_key
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "MAPBOX_PUBLIC_API_KEY"
    value     = var.mapbox_public_api_key
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SENTRY_DSN"
    value     = var.sentry_dsn
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SLACK_INCOMING_WEBHOOK_URL"
    value     = var.slack_incoming_webhook_url
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "ALLOWED_HOSTS"

    # TODO: domain
    value = "*"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_ACCESS_KEY_ID"
    value     = aws_iam_access_key.backend.id
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_SECRET_ACCESS_KEY"
    value     = aws_iam_access_key.backend.secret
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_MEDIA_BUCKET"
    value     = aws_s3_bucket.backend_media.id
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_REGION_NAME"
    value     = aws_s3_bucket.backend_media.region
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "EMAIL_BACKEND"
    value     = "django_ses.SESBackend"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "FRONTEND_URL"
    value     = "https://pycon.it"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "PRETIX_API"
    value     = "https://tickets.pycon.it/api/v1/"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "PRETIX_API_TOKEN"
    value     = var.pretix_api_token
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "PINPOINT_APPLICATION_ID"
    value     = var.pinpoint_application_id
  }

  # google settings

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"
    value     = var.social_auth_google_oauth2_key
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"
    value     = var.social_auth_google_oauth2_secret
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

  # health

  setting {
    namespace = "aws:elasticbeanstalk:healthreporting:system"
    name      = "SystemType"
    value     = "enhanced"
  }

  setting {
    namespace = "aws:elasticbeanstalk:cloudwatch:logs"
    name      = "StreamLogs"
    value     = "true"
  }

  setting {
    namespace = "aws:elasticbeanstalk:cloudwatch:logs:health"
    name      = "HealthStreamingEnabled"
    value     = "true"
  }
}

output "pycon_backend_domain" {
  value = aws_elastic_beanstalk_environment.pycon_env.cname
}
