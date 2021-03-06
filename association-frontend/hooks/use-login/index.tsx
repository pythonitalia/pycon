import { useCallback, useContext } from "react";

// import { UserContext } from "~/components/user-provider";

export const TOKEN_NAME = "auth-token";

export const setLoginState = (token: string) =>
  window.localStorage.setItem(TOKEN_NAME, token);

export const getToken = () => window.localStorage.getItem(TOKEN_NAME);

const getLoginState = () => {
  try {
    const token = getToken();
    if (token) {
      return true;
    }
  } catch {
    return false;
  }
  return false;
};

// export const useUser = () => {
//   const { user, resetUrqlClient } = useContext(UserContext);

//   const logout = useCallback(() => {
//     window.localStorage.removeItem(TOKEN_NAME);
//     resetUrqlClient?.();
//   }, [resetUrqlClient]);

//   return {
//     user,
//     logout,
//     setLoginState,
//   };
// };

export const useLoginState = () => [getLoginState(), setLoginState];
