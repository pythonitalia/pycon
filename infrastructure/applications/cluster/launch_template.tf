resource "aws_launch_template" "pythonit" {
  name          = "pythonit-${terraform.workspace}-server"
  image_id      = "ami-0bd650c1ca04cc1a4" #todo
  instance_type = "t4g.small"
  # user_data     = base64encode(data.template_file.server_user_data.rendered)
  key_name      = "pretix"

  iam_instance_profile {
    name = aws_iam_instance_profile.server.name
  }

  # block_device_mappings {
  #   device_name = data.aws_ami.ecs.root_device_name

  #   ebs {
  #     volume_size = 20
  #   }
  # }

  network_interfaces {
    associate_public_ip_address = true
    security_groups = [
      # data.aws_security_group.rds.id,
      # data.aws_security_group.lambda.id,
      # data.aws_security_group.tempone.id,
      aws_security_group.server.id,
    ]
    subnet_id = data.aws_subnet.public_1a.id
  }
}
