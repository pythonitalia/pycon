resource "aws_lambdaweb_function" "app" {
  function_name = "pythonit-pycon-frontend-${terraform.workspace}"
}
