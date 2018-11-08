resource "aws_s3_bucket" "tsalon-images-bucket" {
    bucket = "tsalon-images"
    acl = "private"
    policy = <<EOF
{
  "Id": "bucket_policy_uploads",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "bucket_policy_uploads_main",
      "Action": [
        "s3:GetObject"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::tsalon-images/*",
      "Principal": "*"
    }
  ]
}
EOF
    website {
        index_document = "index.html"
        error_document = "404.html"
    }
}

resource "aws_s3_bucket" "tsalon-media" {
    bucket = "tsalon-site-media"
    acl = "private"
    policy = <<EOF
{
  "Id": "bucket_policy_media",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "bucket_policy_media_main",
      "Action": [
        "s3:GetObject"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::tsalon-site-media/*",
      "Principal": "*"
    }
  ]
}
EOF
    website {
        index_document = "index.html"
        error_document = "404.html"
    }
}