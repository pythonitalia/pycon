import dotenv from "dotenv";

dotenv.config();

export const {
  // Secrets
  PASTAPORTO_SECRET,
  IDENTITY_SECRET,

  // Services
  USERS_SERVICE,

  // Other configuration
  IS_DEV = false,
  VARIANT = "default",
} = process.env;
