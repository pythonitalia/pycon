resource "aws_sqs_queue" "queue" {
  name                       = "${terraform.workspace}-pycon-backend.fifo"
  fifo_queue                 = true
  visibility_timeout_seconds = local.is_prod ? 60 * 30 : 60 * 5

  tags = {
    Env = terraform.workspace
  }
}

resource "aws_lambda_event_source_mapping" "map_main_lambda_events" {
  event_source_arn = aws_sqs_queue.queue.arn
  function_name    = module.lambda.arn
}
