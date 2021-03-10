resource "aws_iam_role" "lambda_role" {
  name               = "pythonit-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    effect = "Allow"
  }
}

resource "aws_iam_role_policy" "lambda_role" {
  name   = "pythonit-lambda-role-policy"
  role   = aws_iam_role.lambda_role.id
  policy = data.aws_iam_policy_document.lambda_role.json
}

data "aws_iam_policy_document" "lambda_role" {
  # Logs
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["*"]
    effect    = "Allow"
  }

  # EC2 for VPC
  statement {
    actions = [
      "ec2:DescribeNetworkInterfaces",
      "ec2:CreateNetworkInterface",
      "ec2:DeleteNetworkInterface",
      "ec2:AttachNetworkInterface"
    ]
    resources = ["*"]
    effect    = "Allow"
  }
}
