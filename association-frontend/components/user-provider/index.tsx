import { getToken } from "hooks/use-login";
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
  const token = getToken();
  const [{ data, fetching, error }, executeQuery] = useMeQuery({
    requestPolicy: "network-only",
  });
  console.log({ data });

  useEffect(() => {
    console.log(`token is changed!!${token}`);
    const listener = () => {
      console.log("fetching user again");
      executeQuery();
    };

    window.addEventListener("tokenChanged", listener);
    return () => {
      window.removeEventListener("tokenChanged", listener);
    };
  }, [token]);

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
