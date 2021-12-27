resource "aws_cloudwatch_event_rule" "membership_check_status" {
  name                = "${terraform.workspace}-association-backend-membership-check-status"
  description         = "Cronjob checking daily that people have a valid payment for their subscription"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "membership_check_status_to_lambda" {
  arn  = module.lambda.arn
  rule = aws_cloudwatch_event_rule.membership_check_status.id
  input = jsonencode({
    "event" : {
      "name" : "membership.check_status",
      "payload" : {}
    }
  })
}
