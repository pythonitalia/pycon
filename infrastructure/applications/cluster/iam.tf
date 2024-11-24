resource "aws_iam_instance_profile" "server" {
  name = "pythonit-${terraform.workspace}-server"
  role = aws_iam_role.server.name
}

resource "aws_iam_role" "server" {
  name = "pythonit-${terraform.workspace}-server-role"
  assume_role_policy = data.aws_iam_policy_document.server_assume_role.json
}

resource "aws_iam_role_policy" "server" {
  name   = "pythonit-${terraform.workspace}-server-policy"
  role   = aws_iam_role.server.id
  policy = data.aws_iam_policy_document.server_role_policy.json
}

data "aws_iam_policy_document" "server_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com", "ecs-tasks.amazonaws.com", "ecs.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "server_role_policy" {
  statement {
    effect = "Allow"
    actions = [
      "iam:PassRole",
      "ses:*",
      "ecs:*",
      "ecr:*",
    ]
    resources = [
      "*"
    ]
  }

  statement {
    effect    = "Allow"
    actions   = ["cloudwatch:PutMetricData", "logs:*"]
    resources = ["*"]
  }

  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::${terraform.workspace}-pycon-backend-media",
      "arn:aws:s3:::${terraform.workspace}-pycon-backend-media/*",
      "arn:aws:s3:::${terraform.workspace}-pretix-media",
      "arn:aws:s3:::${terraform.workspace}-pretix-media/*",
    ]
  }

  statement {
    actions = [
      "sns:CreatePlatformEndpoint",
      "sns:Publish"
    ]
    resources = ["*"]
    effect    = "Allow"
  }

  statement {
    actions = [
      "sqs:SendMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:ReceiveMessage",
    ]
    resources = ["*"]
    effect    = "Allow"
  }

  statement {
    actions = [
      "ec2:DescribeAvailabilityZones",
      "ec2:DescribeInstances",
      "ec2:CreateVolume",
      "ec2:AttachVolume",
      "ec2:DetachVolume",
      "ec2:CreateTags",
      "ec2:DeleteVolume",
      "ec2:DescribeVolumes",
    ]
    resources = ["*"]
    effect    = "Allow"
  }

  statement {
    actions = [
      "ssmmessages:CreateControlChannel",
      "ssmmessages:CreateDataChannel",
      "ssmmessages:OpenControlChannel",
      "ssmmessages:OpenDataChannel"
    ]
    resources = ["*"]
    effect    = "Allow"
  }
}

output "iam_role_arn" {
  value = aws_iam_role.server.arn
}
