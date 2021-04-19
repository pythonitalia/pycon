import { useCallback, useContext } from "react";

import { UserContext } from "~/components/user-provider";

export const useUser = () => {
  const { user, resetUrqlClient } = useContext(UserContext);
  const logout = useCallback(() => {
    resetUrqlClient?.();
  }, [resetUrqlClient]);

  return {
    user,
    logout,
  };
};
