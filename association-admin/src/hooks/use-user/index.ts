import { useCallback, useContext } from "react";

import { UserContext } from "~/components/user-provider";

export const TOKEN_NAME = "auth-token";

const setToken = (token: string) => {
  window.localStorage.setItem(TOKEN_NAME, token);
  window.dispatchEvent(new Event("tokenChanged"));
};

export const useUser = () => {
  const { user, resetUrqlClient } = useContext(UserContext);
  const logout = useCallback(() => {
    window.localStorage.removeItem(TOKEN_NAME);
    resetUrqlClient?.();
  }, [resetUrqlClient]);

  return {
    user,
    logout,
    setToken,
  };
};

export const getToken = () => window.localStorage.getItem(TOKEN_NAME);
