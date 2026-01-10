resource "aws_sqs_queue" "new_file_uploaded" {
  name = "pythonit-${terraform.workspace}-new-file-uploaded"
  visibility_timeout_seconds = 300
}

resource "aws_sqs_queue_policy" "new_file_uploaded" {
  queue_url = aws_sqs_queue.new_file_uploaded.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "s3.amazonaws.com"
        }
        Action = "sqs:SendMessage"
        Resource = aws_sqs_queue.new_file_uploaded.arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_s3_bucket.backend_media.arn
          }
        }
      }
    ]
  })
}
