resource "aws_s3_bucket" "email_assets" {
  bucket = "pythonit-email-assets"
  acl    = "private"
}
