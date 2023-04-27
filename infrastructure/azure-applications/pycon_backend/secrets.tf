data "azurerm_key_vault_secret" "db_username" {
  name         = "db-username"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "service_to_service_secret" {
  name         = "service-to-service-secret"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "identity_secret" {
  name         = "identity-secret"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "pastaporto_secret" {
  name         = "pastaporto-secret"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "sentry_dsn" {
  name         = "sentry-dsn"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "mapbox_public_api_key" {
  name         = "mapbox-public-api-key"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "volunteers_push_notifications_ios_arn" {
  name         = "volunteers-push-notifications-ios-arn"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "volunteers_push_notifications_android_arn" {
  name         = "volunteers-push-notifications-android-arn"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "speakers_email_address" {
  name         = "speakers-email-address"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "pretix_api_token" {
  name         = "pretix-api-token"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "mailchimp_secret_key" {
  name         = "mailchimp-secret-key"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "mailchimp_dc" {
  name         = "mailchimp-dc"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "mailchimp_list_id" {
  name         = "mailchimp-list-id"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "plain_api_token" {
  name         = "plain-api-token"
  key_vault_id = azurerm_key_vault.vault.id
}

data "azurerm_key_vault_secret" "userid_hash" {
  name         = "userid-hash"
  key_vault_id = azurerm_key_vault.vault.id
}
