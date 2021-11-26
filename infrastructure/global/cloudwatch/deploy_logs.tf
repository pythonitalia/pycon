resource "aws_cloudwatch_log_group" "deploy_logs" {
  name              = "/github/deploy/terraform-logs"
  retention_in_days = 7
}
