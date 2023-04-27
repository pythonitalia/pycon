locals {
  secret_env_vars = [
    for env_var in var.env_vars : {
      name  = lower(replace(env_var.name, "_", "-")),
      value = env_var.value
    }
    if env_var.secret
  ]
  sld_tld = join(".", slice(split(".", var.domain), 1, 3))
}

data "azurerm_container_app_environment" "env" {
  name                = var.environment_name
  resource_group_name = var.resource_group_name
}

data "azurerm_resource_group" "rg" {
  name = var.resource_group_name
}

data "azapi_resource" "env" {
  type                   = "Microsoft.App/managedEnvironments@2022-10-01"
  resource_id            = data.azurerm_container_app_environment.env.id
  response_export_values = ["properties.customDomainConfiguration.customDomainVerificationId"]
}


data "azurerm_container_app_environment_certificate" "certificate" {
  name                         = replace(local.sld_tld, ".", "")
  container_app_environment_id = data.azurerm_container_app_environment.env.id
}

resource "azurerm_container_app" "ca_app" {
  name                         = "pythonit-${var.workspace}-${var.service_name}"
  container_app_environment_id = data.azurerm_container_app_environment.env.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"
  depends_on                   = [aws_route53_record.txt_verification]

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

    dynamic "custom_domain" {
      for_each = var.domain != null ? [1] : []

      content {
        name           = var.domain
        certificate_id = data.azurerm_container_app_environment_certificate.certificate.id
      }
    }

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
        for_each = { for k, v in var.env_vars : k => v if !v.deprecated }

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

data "aws_route53_zone" "zone" {
  name = local.sld_tld
}

resource "aws_route53_record" "txt_verification" {
  count = var.domain != null ? 1 : 0

  zone_id = data.aws_route53_zone.zone.zone_id
  name    = "asuid.${var.domain}"
  type    = "TXT"
  ttl     = "30"
  records = [jsondecode(data.azapi_resource.env.output).properties.customDomainConfiguration.customDomainVerificationId]
}

resource "aws_route53_record" "domain" {
  count = var.domain != null ? 1 : 0

  zone_id = data.aws_route53_zone.zone.zone_id
  name    = var.domain
  type    = "A"
  ttl     = "30"
  records = [data.azurerm_container_app_environment.env.static_ip_address]
}
