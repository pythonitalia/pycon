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
    target_port      = var.port

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  template {
    min_replicas = var.workspace == "production" ? 1 : 0
    max_replicas = 1

    container {
      name    = "main"
      image   = "ghcr.io/pythonitalia/pycon/${var.service_name}:${var.githash}"
      command = var.command
      cpu     = 1
      memory  = "2Gi"

      dynamic "env" {
        for_each = var.env_vars

        content {
          name        = env.value.name
          value       = env.value.value
          secret_name = env.value.secret ? lower(replace(env.value.name, "_", "-")) : null
        }
      }

      # liveness_probe {
      #   transport        = "HTTP"
      #   path             = var.healthcheck_path
      #   port             = var.port
      #   interval_seconds = 1
      #   initial_delay    = 3
      # }

      # startup_probe {
      #   transport        = "HTTP"
      #   path             = var.healthcheck_path
      #   port             = var.port
      #   interval_seconds = 1
      # }

      # readiness_probe {
      #   transport               = "HTTP"
      #   path                    = var.healthcheck_path
      #   port                    = var.port
      #   interval_seconds        = 1
      #   success_count_threshold = 1
      # }
    }
  }
}
