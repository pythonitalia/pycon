locals {
  email_tracking_domain = "mail-${terraform.workspace}.python.it"
}

resource "aws_sesv2_configuration_set" "main" {
  configuration_set_name = "pythonit-${terraform.workspace}"

  tracking_options {
    custom_redirect_domain = local.email_tracking_domain
  }
}

resource "aws_sesv2_configuration_set_event_destination" "backend" {
  event_destination_name = "backend"
  configuration_set_name = aws_sesv2_configuration_set.main.configuration_set_name

  event_destination {
    sns_destination {
      topic_arn = aws_sns_topic.emails_updates.arn
    }
    enabled              = true
    matching_event_types = [
      "BOUNCE",
      "CLICK",
      "COMPLAINT",
      "DELIVERY",
      "DELIVERY_DELAY",
      "OPEN",
      "REJECT",
      "RENDERING_FAILURE",
      "SEND",
      "SUBSCRIPTION",
    ]
  }
}
