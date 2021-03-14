import { PYCON_BACKEND, USERS_SERVICE, VARIANT } from "./config";

const DEFAULT_SERVICES = [
  {
    name: "users",
    url: `${USERS_SERVICE}/graphql`,
  },
  {
    name: "pycon-backend",
    url: `${PYCON_BACKEND}/graphql`,
  },
];

const ADMIN_SERVICES = [
  {
    name: "users:admin",
    url: `${USERS_SERVICE}/admin-api`,
  },
];

export const getServices = () => {
  if (VARIANT === "admin") {
    return ADMIN_SERVICES;
  }

  return DEFAULT_SERVICES;
};
