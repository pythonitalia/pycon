locals {
  load_balancer_user_data = templatefile("${path.module}/userdata.sh", {
    ecs_cluster = aws_ecs_cluster.cluster.name
    swap_size = "1G"
    role = "load_balancer"
  })
}

resource "aws_instance" "load_balancer" {
  ami               = "ami-09c79d1104c5634b4" #todo
  instance_type     = "t4g.nano"
  subnet_id         = data.aws_subnet.public_1a.id
  availability_zone = "eu-central-1a"
  vpc_security_group_ids = [
    aws_security_group.load_balancer.id,
  ]
  source_dest_check    = false
  user_data            = local.load_balancer_user_data
  iam_instance_profile = aws_iam_instance_profile.load_balancer.name
  key_name             = "pretix"
  user_data_replace_on_change = true

  root_block_device {
    volume_size = 30
  }

  tags = {
    Name = "pythonit-${terraform.workspace}-load-balancer"
    Role = "load_balancer"
  }
}

output "load_balancer_public_ip" {
  value = aws_instance.load_balancer.public_ip
}
