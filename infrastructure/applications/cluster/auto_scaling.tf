resource "aws_autoscaling_group" "server" {
  name                  = "pythonit-${terraform.workspace}-server"
  vpc_zone_identifier   = [data.aws_subnet.public_1a.id]
  desired_capacity      = 1
  max_size              = 1
  min_size              = 1
  termination_policies  = ["OldestInstance"]
  protect_from_scale_in = true

  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage       = 100
      max_healthy_percentage       = 110
      scale_in_protected_instances = "Refresh"
      instance_warmup              = 30
    }
  }

  launch_template {
    id      = aws_launch_template.pythonit.id
    version = aws_launch_template.pythonit.latest_version
  }

  tag {
    key                 = "Name"
    value               = "pythonit-${terraform.workspace}-server"
    propagate_at_launch = true
  }

  tag {
    key                 = "AmazonECSManaged"
    value               = true
    propagate_at_launch = true
  }
}
