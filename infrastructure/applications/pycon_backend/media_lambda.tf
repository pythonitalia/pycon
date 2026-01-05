resource "aws_lambda_function" "new_file_uploaded" {
  function_name = "pythonit-${terraform.workspace}-new-file-uploaded"
  package_type = "Image"
  image_uri = "${data.aws_ecr_repository.be_repo.repository_url}@${data.aws_ecr_image.be_arm_image.image_digest}"
  architectures = ["arm64"]
  memory_size = 2048
  timeout = 300
  role = var.iam_role_arn

  environment {
    variables = {
      for variable in local.env_vars:
        variable.name => variable.value
        if variable.name != "AWS_DEFAULT_REGION"
    }
  }
}

resource "aws_lambda_event_source_mapping" "new_file_uploaded" {
  event_source_arn = aws_sqs_queue.new_file_uploaded.arn
  function_name = aws_lambda_function.new_file_uploaded.function_name
  enabled = true
}
