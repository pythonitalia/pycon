import { createContext } from "react";

import { MeQuery, useMeQuery } from "./me.generated";

type UserContext = {
  user: MeQuery["me"] | null;
};

export const UserContext = createContext<UserContext>({
  user: null,
});

export const UserProvider: React.FC = ({ children }) => {
  const [{ data, fetching, error }] = useMeQuery();

  return (
    <UserContext.Provider
      value={{
        user: data && data.me,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};
