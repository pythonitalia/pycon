resource "aws_s3_bucket" "media" {
  bucket        = "pythonit-${terraform.workspace}-pretix-media"
  force_destroy = !local.is_prod
}

resource "aws_s3_bucket_server_side_encryption_configuration" "media" {
  bucket = aws_s3_bucket.media.id

  rule {
    bucket_key_enabled = false
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_cors_configuration" "cors" {
  bucket = aws_s3_bucket.media.id

  cors_rule {
    allowed_methods = ["GET"]
    allowed_origins = [
      "https://${local.alias}"
    ]
  }
}
