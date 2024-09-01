data "aws_sesv2_configuration_set" "main" {
  configuration_set_name = "pythonit-${terraform.workspace}"
}
