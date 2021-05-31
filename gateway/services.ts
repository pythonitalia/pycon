import {
  USERS_SERVICE,
  ASSOCIATION_BACKEND_SERVICE,
  PYCON_BACKEND_SERVICE,
  VARIANT,
} from "./config";

const DEFAULT_SERVICES = [
  {
    name: "users-backend",
    url: `${USERS_SERVICE}/graphql`,
  },
  {
    name: "association-backend",
    url: `${ASSOCIATION_BACKEND_SERVICE}/graphql`,
  },
  {
    name: "pycon-backend",
    url: `${PYCON_BACKEND_SERVICE}/graphql`,
  },
  {
    name: "logout",
    url: `http://logout.service`,
  },
];

const ADMIN_SERVICES = [
  {
    name: "users-backend:admin",
    url: `${USERS_SERVICE}/admin-api`,
  },
  {
    name: "association-backend:admin",
    url: `${ASSOCIATION_BACKEND_SERVICE}/admin-api`,
  },
  {
    name: "logout",
    url: `http://logout.service`,
  },
];

export const getServices = () => {
  if (VARIANT === "admin") {
    return ADMIN_SERVICES;
  }

  return DEFAULT_SERVICES;
};
