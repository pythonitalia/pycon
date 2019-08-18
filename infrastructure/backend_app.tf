resource "aws_vpc" "default" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "primary" {
  vpc_id                  = "${aws_vpc.default.id}"
  availability_zone       = "eu-central-1a"
  cidr_block              = "10.0.4.0/24"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "secondary" {
  vpc_id                  = "${aws_vpc.default.id}"
  availability_zone       = "eu-central-1b"
  cidr_block              = "10.0.5.0/24"
  map_public_ip_on_launch = true
}

# SECURITY GROUP

resource "aws_security_group" "backend_rds" {
  vpc_id      = "${aws_vpc.default.id}"
  name        = "${terraform.workspace}_backend_rds"
  description = "Allow inbound postgres traffic"
}

resource "aws_security_group_rule" "allow_postgres" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = "${aws_security_group.backend_rds.id}"
  source_security_group_id = "${aws_security_group.backend_rds.id}"
}

# DATABASE

variable "database_password" {}
variable "secret_key" {}

resource "aws_db_instance" "backend" {
  allocated_storage   = 10
  storage_type        = "gp2"
  engine              = "postgres"
  engine_version      = "9.6.6"
  instance_class      = "db.t2.micro"
  name                = "${terraform.workspace}backend"
  username            = "root"
  password            = "${var.database_password}"
  multi_az            = "false"
  availability_zone   = "eu-central-1a"
  skip_final_snapshot = true

  db_subnet_group_name   = "${aws_db_subnet_group.backend_rds.name}"
  vpc_security_group_ids = ["${aws_security_group.backend_rds.id}"]
}

resource "aws_db_subnet_group" "backend_rds" {
  name       = "${terraform.workspace}_backend_rds"
  subnet_ids = ["${aws_subnet.primary.id}", "${aws_subnet.secondary.id}"]
}

# INTERNET GATEWAY

resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.default.id}"
}

resource "aws_route" "internet_access" {
  route_table_id         = "${aws_vpc.default.main_route_table_id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.default.id}"
}

# ROLE

resource "aws_iam_instance_profile" "pycon" {
  name = "ng-beanstalk-ec2-user-${terraform.workspace}"
  role = "${aws_iam_role.pycon.name}"
}

resource "aws_iam_role" "pycon" {
  name = "ng-beanstalk-ec2-role-${terraform.workspace}"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "pycon" {
  name = "pycon_with_ECR"
  role = "${aws_iam_role.pycon.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "cloudwatch:PutMetricData",
        "ds:CreateComputer",
        "ds:DescribeDirectories",
        "ec2:DescribeInstanceStatus",
        "logs:*",
        "ssm:*",
        "ec2messages:*",
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:GetRepositoryPolicy",
        "ecr:DescribeRepositories",
        "ecr:ListImages",
        "ecr:DescribeImages",
        "ecr:BatchGetImage",
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

# Elastic Beanstalk application

resource "aws_elastic_beanstalk_application" "pycon" {
  name        = "pycon"
  description = "pycon"
}

resource "aws_elastic_beanstalk_environment" "pycon_env" {
  name                = "${terraform.workspace}-env"
  application         = "${aws_elastic_beanstalk_application.pycon.name}"
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
    name      = "DATABASE_URL"
    value     = "postgres://${aws_db_instance.backend.username}:${aws_db_instance.backend.password}@${aws_db_instance.backend.address}:${aws_db_instance.backend.port}/${aws_db_instance.backend.name}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SECRET_KEY"
    value     = "${var.secret_key}"
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
    value     = "${aws_iam_access_key.backend.id}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_SECRET_ACCESS_KEY"
    value     = "${aws_iam_access_key.backend.secret}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_MEDIA_BUCKET"
    value     = "${aws_s3_bucket.backend_media.id}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "AWS_REGION_NAME"
    value     = "${aws_s3_bucket.backend_media.region}"
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

output "pycon_backend_domain" {
  value = "${aws_elastic_beanstalk_environment.pycon_env.cname}"
}
