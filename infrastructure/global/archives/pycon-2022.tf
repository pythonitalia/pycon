resource "aws_s3_bucket" "archive_2022" {
  bucket = "2022.pycon.it"
  acl    = "private"

  website {
    index_document = "index.html"
  }
}
