locals {
  secret_env_vars = [
    for env_var in var.env_vars : {
      name  = lower(replace(env_var.name, "_", "-")),
      value = env_var.value
    }
    if env_var.secret
  ]
}

data "azurerm_container_app_environment" "env" {
  name                = var.environment_name
  resource_group_name = var.resource_group_name
}

resource "azurerm_container_app" "ca_app" {
  name                         = "pythonit-${var.workspace}-${var.service_name}"
  container_app_environment_id = data.azurerm_container_app_environment.env.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  dynamic "secret" {
    for_each = local.secret_env_vars
    content {
      name  = secret.value.name
      value = secret.value.value
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8080
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name    = "main"
      image   = "ghcr.io/pythonitalia/pycon/${var.service_name}:${var.githash}"
      command = ["/home/app/.venv/bin/python", "-m", "gunicorn", "-w", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "main:wrapped_app", "--bind", "0.0.0.0:8000"]
      cpu     = 0.5
      memory  = "1Gi"

      dynamic "env" {
        for_each = var.env_vars

        content {
          name        = env.value.name
          value       = env.value.value
          secret_name = env.value.secret ? lower(replace(env.value.name, "_", "-")) : null
        }
      }

      liveness_probe {
        transport        = "HTTP"
        path             = "/graphql"
        port             = 8000
        initial_delay    = 7
        interval_seconds = 3
      }

      startup_probe {
        transport        = "HTTP"
        path             = "/graphql"
        port             = 8000
        interval_seconds = 3
      }

      readiness_probe {
        transport        = "HTTP"
        path             = "/graphql"
        port             = 8000
        interval_seconds = 3
      }
    }
  }
}
