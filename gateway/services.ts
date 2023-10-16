import {
  ASSOCIATION_BACKEND_SERVICE,
  PYCON_BACKEND_SERVICE,
  CMS_SERVICE,
} from "./config";

const DEFAULT_SERVICES = [
  {
    name: "association-backend",
    url: `${ASSOCIATION_BACKEND_SERVICE}/graphql`,
  },
  {
    name: "pycon-backend",
    url: `${PYCON_BACKEND_SERVICE}/graphql`,
  },
  {
    name: "cms",
    url: `${CMS_SERVICE}/graphql/`,
  },
];

export const getServices = () => {
  return DEFAULT_SERVICES;
};
