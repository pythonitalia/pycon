data "template_file" "server_user_data" {
  template = file("${path.module}/server_user_data.sh")
  vars = {
    ecs_cluster = aws_ecs_cluster.server.name
  }
}

data "aws_ami" "ecs" {
  owners           = ["self"]

  filter {
    name   = "image-id"
    values = [var.ecs_arm_ami]
  }
}

data "aws_security_group" "tempone" {
  name        = "pythonit-${terraform.workspace}-worker-instance"
}

resource "aws_launch_template" "server" {
  name = "pythonit-${terraform.workspace}-server"
  image_id      = var.ecs_arm_ami
  instance_type = "t4g.medium"
  user_data = base64encode(data.template_file.server_user_data.rendered)
  key_name = "pretix"

  iam_instance_profile {
    name = aws_iam_instance_profile.server.name
  }

  block_device_mappings {
    device_name = data.aws_ami.ecs.root_device_name

    ebs {
      volume_size = 20
    }
  }

  network_interfaces {
    associate_public_ip_address = true
    security_groups = [
      data.aws_security_group.rds.id,
    data.aws_security_group.lambda.id,
    data.aws_security_group.tempone.id,
    aws_security_group.server.id,
    ]
    subnet_id = data.aws_subnet.public_1a.id
  }
}

resource "aws_autoscaling_group" "server" {
  name = "pythonit-${terraform.workspace}-server"
  vpc_zone_identifier = [data.aws_subnet.public_1a.id]
  desired_capacity   = 1
  max_size           = 1
  min_size           = 1
  termination_policies = ["OldestInstance"]
  protect_from_scale_in = true

  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 100
      max_healthy_percentage = 110
      scale_in_protected_instances = "Refresh"
      instance_warmup = 30
    }
  }

  launch_template {
    id      = aws_launch_template.server.id
    version = aws_launch_template.server.latest_version
  }

  tag {
    key                = "Name"
    value               = "pythonit-${terraform.workspace}-server"
    propagate_at_launch = true
  }

  tag {
    key                 = "AmazonECSManaged"
    value               = true
    propagate_at_launch = true
  }
}
