import { useQuery } from "@apollo/react-hooks";

import { CurrentUserQuery } from "../generated/graphql-backend";
import CURRENT_USER_QUERY from "./current-user.graphql";

export const useCurrentUser = () => {
  const { loading, error, data } = useQuery<CurrentUserQuery>(
    CURRENT_USER_QUERY,
    {
      errorPolicy: "all",
    },
  );

  const user = data && data.me;

  return { loading, error, user };
};
