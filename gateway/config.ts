import dotenv from "dotenv";

dotenv.config();

export const {
  // Secrets
  PASTAPORTO_SECRET,
  IDENTITY_SECRET,
  SERVICE_TO_SERVICE_SECRET,

  // Services
  USERS_SERVICE,
  ASSOCIATION_BACKEND_SERVICE,
  PYCON_BACKEND_SERVICE,
  CMS_SERVICE,

  // Other configuration
  IS_DEV = process.env.NODE_ENV === "development",
  SENTRY_DSN = "",
  ENV = "local",
} = process.env;
