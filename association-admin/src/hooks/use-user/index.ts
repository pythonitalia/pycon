import { useContext } from "react";

import { UserContext } from "~/components/user-provider";

export const TOKEN_NAME = "auth-token";

const logout = () => window.localStorage.removeItem(TOKEN_NAME);
const setToken = (token: string) =>
  window.localStorage.setItem(TOKEN_NAME, token);

export const useUser = () => {
  const value = useContext(UserContext);

  return {
    user: value.user,
    logout,
    setToken,
  };
};

export const getToken = () => window.localStorage.getItem(TOKEN_NAME);
