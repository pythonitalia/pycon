import {
  ASSOCIATION_BACKEND_SERVICE,
  PYCON_BACKEND_SERVICE,
  USERS_SERVICE,
  VARIANT,
} from "./config";

const DEFAULT_SERVICES = [
  {
    name: "users",
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
