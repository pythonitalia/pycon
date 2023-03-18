resource "azuread_user" "marco" {
  user_principal_name  = "marco@pythonitalia.onmicrosoft.com"
  display_name         = "Marco Acierno"
  mail_nickname        = "marco"
  show_in_address_list = false
}
