locals {
  secret_env_vars = [
    for env_var in var.env_vars : {
      name  = lower(replace(env_var.name, "_", "-")),
      value = env_var.value
    }
    if env_var.secret
  ]
}

data "azapi_resource" "ca_env" {
  name      = "pythonit-${var.workspace}-ca-env"
  parent_id = var.resource_group_id
  type      = "Microsoft.App/managedEnvironments@2022-03-01"

  response_export_values = [
    "id",
  ]
}

resource "azapi_resource" "ca_app" {
  type      = "Microsoft.App/containerApps@2022-03-01"
  parent_id = var.resource_group_id
  location  = "westeurope"
  name      = "pythonit-${var.workspace}-${var.service_name}"

  body = jsonencode({
    properties = {
      managedEnvironmentId = data.azapi_resource.ca_env.id
      configuration = {
        ingress = {
          external   = true
          targetPort = 8000
        }
        secrets = local.secret_env_vars
      }
      template = {
        containers = [
          {
            name    = "main"
            image   = "ghcr.io/pythonitalia/pycon/${var.service_name}:${var.githash}"
            command = ["/home/app/.venv/bin/python", "-m", "gunicorn", "-w", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "main:wrapped_app", "--bind", "0.0.0.0:8000"]

            resources = {
              cpu    = 1
              memory = "2Gi"
            }

            probes = [
              {
                type = "Liveness"
                httpGet = {
                  path = "/graphql"
                  port = 8000
                }
                initialDelaySeconds = 7
                periodSeconds       = 3
              },
              {
                type = "Startup"
                httpGet = {
                  path = "/graphql"
                  port = 8000
                }
                initialDelaySeconds = 3
                periodSeconds       = 3
              },
              {
                type = "Readiness"
                tcpSocket = {
                  port = 8000
                }
                initialDelaySeconds = 10
                periodSeconds       = 3
              }
            ]

            env = [
              for env_var in var.env_vars : {
                name      = env_var.name,
                value     = env_var.value
                secretRef = env_var.secret ? lower(replace(env_var.name, "_", "-")) : null
              }
            ]
          }
        ]
        scale = {
          minReplicas = 0
          maxReplicas = 1
        }
      }
    }
  })
}
