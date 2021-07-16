data "external" "secrets" {
  program = ["python", "${path.module}/secrets.py"]

  query = {
    workspace = terraform.workspace
    service = var.service
  }
}

output "value" {
  value = data.external.secrets.result
  # sensitive = true
}
