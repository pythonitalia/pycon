const VARIANT = process.env.VARIANT || "default";

const DEFAULT_SERVICES = [
  {
    name: "users",
    url: "http://localhost:8050/graphql",
  },
];

const ADMIN_SERVICES = [
  {
    name: "users:admin",
    url: "http://localhost:8050/admin-api",
  },
];

export const getServices = () => {
  if (VARIANT === "admin") {
    return ADMIN_SERVICES;
  }

  return DEFAULT_SERVICES;
};

export const getPort = () => {
  return VARIANT === "admin" ? 4001 : 4000;
};
