resource "aws_s3_bucket" "backend_media" {
  bucket        = "${terraform.workspace}-pycon-backend-media"
  force_destroy = !local.is_prod
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backend_media" {
  bucket = aws_s3_bucket.backend_media.id

  rule {
    bucket_key_enabled = false
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_notification" "new_file_uploaded" {
  bucket = aws_s3_bucket.backend_media.id

  queue {
    queue_arn = aws_sqs_queue.new_file_uploaded.arn
    events = ["s3:ObjectCreated:*"]
    filter_prefix = "files/"
  }
}
