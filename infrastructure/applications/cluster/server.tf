locals {
  server_user_data = templatefile("${path.module}/userdata.sh", {
    ecs_cluster = aws_ecs_cluster.cluster.name
    swap_size = "1G"
  })
}

resource "aws_eip" "server" {
  instance = aws_instance.server.id
  domain   = "vpc"
}

resource "aws_instance" "server" {
  ami               = "ami-01c0b647efcf28a90"
  instance_type     = "t4g.small"
  subnet_id         = data.aws_subnet.public_1a.id
  availability_zone = "eu-central-1a"
  vpc_security_group_ids = [
    aws_security_group.server.id,
  ]
  source_dest_check    = false
  user_data            = local.server_user_data
  iam_instance_profile = aws_iam_instance_profile.server.name
  key_name             = "pretix"
  user_data_replace_on_change = true

  root_block_device {
    volume_size = 30
  }

  tags = {
    Name = "pythonit-${terraform.workspace}-server"
    Role = "server"
  }
}

resource "aws_ebs_volume" "redis_data" {
  availability_zone = "eu-central-1a"
  size              = 10
  type              = "gp3"

  tags = {
    Name = "redis-data"
  }
}

resource "aws_volume_attachment" "redis_data_attachment" {
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.redis_data.id
  instance_id = aws_instance.server.id
}

output "server_ip" {
  value = aws_instance.server.private_ip
}
