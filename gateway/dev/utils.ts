import { VARIANT } from "../config";

export const getPort = () => {
  return VARIANT === "admin" ? 4001 : 4000;
};
