data "azuread_client_config" "current" {}

resource "azuread_group" "devs" {
  display_name     = "devs"
  owners           = [data.azuread_client_config.current.object_id]
  members          = [azuread_user.marco.object_id]
  security_enabled = true
}
