resource "aws_ses_configuration_set" "main" {
  name = "pythonit-${terraform.workspace}"
  reputation_metrics_enabled = true
  sending_enabled = true
}

resource "aws_ses_event_destination" "be" {
  name                   = "backend"
  configuration_set_name = aws_ses_configuration_set.main.name
  enabled                = true
  matching_types         = ["bounce", "complaint"]

  sns_destination {
    topic_arn = aws_sns_topic.emails_updates.arn
  }
}
