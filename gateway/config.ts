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
  ASSOCIATION_BACKEND_SERVICE,
  PYCON_BACKEND_SERVICE,

  // Other configuration
  IS_DEV = process.env.NODE_ENV === "development",
  VARIANT = "default",
} = process.env;
