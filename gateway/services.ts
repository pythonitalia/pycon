import { PYCON_BACKEND_SERVICE } from "./config";

const DEFAULT_SERVICES = [
  {
    name: "pycon-backend",
    url: `${PYCON_BACKEND_SERVICE}/graphql`,
  },
];

export const getServices = () => {
  return DEFAULT_SERVICES;
};
