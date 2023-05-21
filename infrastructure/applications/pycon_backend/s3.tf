resource "aws_s3_bucket" "backend_media" {
  bucket        = "${terraform.workspace}-pycon-backend-media"
  force_destroy = !local.is_prod

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "badge_scanner_lifecycle" {
  rule {
    id      = "delete-badge-scanner-files"
    status  = "Enabled"

    expiration {
      days = 1
    }

    filter {
      prefix = "badge_scan_exports/"
    }
  }
}
