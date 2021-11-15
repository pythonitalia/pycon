resource "aws_sqs_queue" "cfp_queue" {
  name       = "${terraform.workspace}-pycon-backend-cfp-queue.fifo"
  fifo_queue = true

  tags = {
    Env = terraform.workspace
  }
}
