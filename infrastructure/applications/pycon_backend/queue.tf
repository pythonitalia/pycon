resource "aws_sqs_queue" "queue" {
  name       = "${terraform.workspace}-pycon-backend.fifo"
  fifo_queue = true

  tags = {
    Env = terraform.workspace
  }
}

resource "aws_lambda_event_source_mapping" "map_main_lambda_events" {
  event_source_arn = aws_sqs_queue.queue.arn
  function_name    = module.lambda.arn
}
