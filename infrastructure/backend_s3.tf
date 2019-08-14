resource "aws_s3_bucket" "backend_media" {
  bucket = "${terraform.workspace}-pycon-backend-media"

    cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}
