import { createContext, useEffect } from "react";

import { MeQuery, useMeQuery } from "./me.generated";

type UserContext = {
  user: MeQuery["me"] | null;
};

export const UserContext = createContext<UserContext>({
  user: null,
});

export const UserProvider = ({ children }) => {
  const [{ data }, refetchMe] = useMeQuery({
    requestPolicy: "network-only",
  });

  useEffect(() => {
    const listener = () => {
      refetchMe();
    };
    window.addEventListener("userLoggedIn", listener);
    return () => {
      window.removeEventListener("userLoggedIn", listener);
    };
  }, []);

  return (
    <UserContext.Provider
      value={{
        user: data?.me ?? null,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};
