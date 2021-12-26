resource "aws_cloudwatch_event_rule" "membership_check_expiration" {
  name                = "${terraform.workspace}-association-backend-membership-check-expiration"
  description         = "Cronjob checking daily that people have a valid payment for their subscription"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "membership_check_expiration_to_lambda" {
  arn  = module.lambda.arn
  rule = aws_cloudwatch_event_rule.membership_check_expiration.id
  input = jsonencode({
    "event" : {
      "name" : "membership.check_expiration",
      "payload" : {}
    }
  })
}
