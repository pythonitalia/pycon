resource "aws_s3_bucket" "docker_cache" {
  bucket = "pythonit-docker-cache"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "docker_cache" {
  bucket = aws_s3_bucket.docker_cache.id

  rule {
    bucket_key_enabled = false
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "docker_cache" {
  bucket = aws_s3_bucket.docker_cache.id

  rule {
    id     = "expire-old-cache"
    status = "Enabled"

    expiration {
      days = 30
    }
  }
}

output "docker_cache_bucket_name" {
  value = aws_s3_bucket.docker_cache.bucket
}
