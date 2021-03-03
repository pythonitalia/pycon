import dotenv from "dotenv";

dotenv.config();

export const {
  USERS_SERVICE,
  IS_DEV = false,
  VARIANT = "default",
} = process.env;
