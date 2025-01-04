resource "random_password" "webhook_secret" {
  length           = 64
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "github_repository_webhook" "github_runner_notify" {
  repository = data.github_repository.pycon.name
  events = ["workflow_job"]
  active = true

  configuration {
    url          = aws_lambda_function_url.github_runner_webhook.function_url
    secret = random_password.webhook_secret.result
    content_type = "json"
  }
}
