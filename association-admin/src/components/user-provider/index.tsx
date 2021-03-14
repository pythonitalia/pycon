import { createContext, useEffect } from "react";

import { MeQuery, useMeQuery } from "./me.generated";

type UserContext = {
  user: MeQuery["me"] | null;
  resetUrqlClient: () => void | null;
};

export const UserContext = createContext<UserContext>({
  user: null,
  resetUrqlClient: null,
});

export const UserProvider: React.FC<{ resetUrqlClient: () => void }> = ({
  children,
  resetUrqlClient,
}) => {
  const [{ data, fetching, error }, refetchMe] = useMeQuery({
    requestPolicy: "network-only",
  });

  useEffect(() => {
    const listener = () => refetchMe();
    window.addEventListener("userLoggedIn", listener);
    return () => {
      window.removeEventListener("userLoggedIn", listener);
    };
  }, []);

  return (
    <UserContext.Provider
      value={{
        user: data && data.me,
        resetUrqlClient,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};
