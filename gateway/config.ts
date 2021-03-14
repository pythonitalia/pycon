import dotenv from "dotenv";

dotenv.config();

export const {
  // Secrets
  PASTAPORTO_SECRET,
  IDENTITY_SECRET,
  SERVICE_TO_SERVICE_SECRET,
  PASTAPORTO_ACTION_SECRET,

  // Services
  USERS_SERVICE,
  PYCON_BACKEND,

  // Other configuration
  IS_DEV = false,
  VARIANT = "default",
} = process.env;
