locals {
  admin_domain = terraform.workspace == "production" ? "admin.pycon.it" : "${terraform.workspace}-admin.pycon.it"
  sns_webhook_secret = module.common_secrets.value.sns_webhook_secret
}

resource "aws_sns_topic" "emails_updates" {
  name = "pythonit-${terraform.workspace}-emails-updates"
}

resource "aws_sns_topic_subscription" "backend" {
  topic_arn = aws_sns_topic.emails_updates.arn
  protocol  = "https"
  endpoint  = "https://${local.admin_domain}/notifications/sns-webhook/?api_key=${local.sns_webhook_secret}"
}
