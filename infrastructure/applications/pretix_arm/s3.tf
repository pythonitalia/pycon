locals {
  is_prod = terraform.workspace == "production"
}

resource "aws_s3_bucket" "media" {
  bucket        = "${terraform.workspace}-pretix-media"
  force_destroy = !local.is_prod
}
