resource "aws_sesv2_configuration_set" "main" {
  configuration_set_name = "pythonit-${terraform.workspace}"
}

resource "aws_sesv2_configuration_set_event_destination" "backend" {
  event_destination_name = "backend"
  configuration_set_name = aws_sesv2_configuration_set.main.configuration_set_name

  event_destination {
    sns_destination {
      topic_arn = aws_sns_topic.emails_updates.arn
    }
    enabled              = true
    matching_event_types = ["SEND", "REJECT", "BOUNCE", "COMPLAINT", "DELIVERY", "RENDERING_FAILURE", "DELIVERY_DELAY", "SUBSCRIPTION"]
  }
}
