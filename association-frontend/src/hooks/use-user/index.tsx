import { useCallback, useContext } from "react";

import { UserContext } from "~/components/user-provider";

export const useUser = () => {
  const { user } = useContext(UserContext);
  const logout = useCallback(() => {
    window.location.reload();
  }, []);

  return {
    user,
    logout,
  };
};
