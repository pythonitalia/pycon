resource "aws_iam_role" "load_balancer" {
  name = "pythonit-${terraform.workspace}-load-balancer"
  assume_role_policy = data.aws_iam_policy_document.lb_assume_role.json
}

resource "aws_iam_instance_profile" "load_balancer" {
  name = "pythonit-${terraform.workspace}-load-balancer"
  role = aws_iam_role.load_balancer.name
}

data "aws_iam_policy_document" "lb_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com", "ecs-tasks.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role_policy" "lb" {
  name   = "pythonit-${terraform.workspace}-load-balancer-policy"
  role   = aws_iam_role.load_balancer.id
  policy = data.aws_iam_policy_document.lb_role_policy.json
}

data "aws_iam_policy_document" "lb_role_policy" {
  statement {
    effect = "Allow"
    actions = [
      "iam:PassRole",
      "ecs:*",
      "ecr:*",
      "ec2:DescribeInstances",
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
}
