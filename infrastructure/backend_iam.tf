resource "aws_iam_user" "backend" {
  name = "${terraform.workspace}-backend"
}

resource "aws_iam_access_key" "backend" {
  user = "${aws_iam_user.backend.name}"
}

resource "aws_iam_user_policy" "backend" {
  name = "${terraform.workspace}-backend-media-s3"
  user = "${aws_iam_user.backend.name}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation",
        "s3:ListBucketMultipartUploads",
        "s3:ListBucketVersions"
      ],
      "Resource": "${aws_s3_bucket.backend_media.arn}"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:*Object*",
        "s3:ListMultipartUploadParts",
        "s3:AbortMultipartUpload"
      ],
      "Resource": "${aws_s3_bucket.backend_media.arn}/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sqs:*"
      ],
      "Resource": "arn:aws:sqs:*"
    }
  ]
}

EOF
}

output "backend_access_key" {
  value = "${aws_iam_access_key.backend.id}"
}

output "backend_secret" {
  value = "${aws_iam_access_key.backend.secret}"
}
