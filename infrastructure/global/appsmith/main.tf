resource "aws_instance" "main" {
  ami               = "ami-0cf11524536d89b14"
  instance_type     = "t3.small"
  subnet_id         = data.aws_subnet.public.id
  availability_zone = "eu-central-1a"
  vpc_security_group_ids = [
    aws_security_group.instance.id,
    data.aws_security_group.rds.id
  ]
  source_dest_check    = false
  iam_instance_profile = aws_iam_instance_profile.instance.name
  key_name             = "pretix"

  tags = {
    Name = "appsmith-instance"
  }
}

resource "aws_eip" "ip" {
  instance = aws_instance.main.id
  vpc      = true
  tags = {
    Name = "appsmith"
  }
}
