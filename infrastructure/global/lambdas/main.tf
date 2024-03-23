resource "aws_iam_role" "lambda_edge_exec" {
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": ["lambda.amazonaws.com", "edgelambda.amazonaws.com"]
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

data "archive_file" "forward_host_code" {
  type        = "zip"
  output_path = "/tmp/forward_host_code.zip"
  source {
    content  = <<EOF
export function handler(event, context, callback) {
    const request = event.Records[0].cf.request;

    request.headers['x-forwarded-host'] = [{
        key: 'X-Forwarded-Host',
        value: request.headers.host[0].value
    }];

    return callback(null, request);
};
EOF
    filename = "index.js"
  }
}


resource "aws_lambda_function" "forward_host_header" {
  function_name = "forward_host_header"
  role          = aws_iam_role.lambda_edge_exec.arn
  handler       = "index.handler"
  filename         = data.archive_file.forward_host_code.output_path
  source_code_hash = data.archive_file.forward_host_code.output_base64sha256
  runtime = "nodejs20.x"
  publish = true
  provider = aws.us
  architectures = ["arm64"]
}
