import {
  ASSOCIATION_BACKEND_SERVICE,
  PYCON_BACKEND_SERVICE,
  USERS_SERVICE,
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

export const getServices = () => {
  return DEFAULT_SERVICES;
};
