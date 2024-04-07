resource "aws_ecs_cluster" "server" {
  name = "pythonit-${terraform.workspace}-server"
}

data "template_file" "user_data" {
  template = file("${path.module}/user_data.sh")
  vars = {
    ecs_cluster        = aws_ecs_cluster.server.name
    tailscale_auth_key = module.common_secrets.value.tailscale_auth_key
  }
}

data "aws_ami" "ecs" {
  most_recent = true

  filter {
    name   = "name"
    values = ["al2023-ami-ecs-hvm-2023.0.20240328-kernel-6.1-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["amazon"]
}

resource "aws_instance" "server" {
  ami               = data.aws_ami.ecs.id
  instance_type     = "t3a.medium"
  subnet_id         = data.aws_subnet.public.id
  availability_zone = "eu-central-1a"
  vpc_security_group_ids = [
    aws_security_group.instance.id,
    data.aws_security_group.rds.id
  ]
  source_dest_check    = false
  user_data            = data.template_file.user_data.rendered
  iam_instance_profile = aws_iam_instance_profile.instance.name
  key_name             = "pretix"

  tags = {
    Name = "pythonit-${terraform.workspace}-server"
  }

  credit_specification {
    cpu_credits = "standard"
  }
}
