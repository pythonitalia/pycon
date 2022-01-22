import { useEffect } from "react";

import { USER_INFO_CACHE } from "~/components/profile/hooks";
import { CurrentUserQueryResult, useCurrentUserQuery } from "~/types";

import { updateOlarkFields } from "./olark";

type CurrentUser = {
  loading: boolean;
  error: any;
  user?: CurrentUserQueryResult["data"]["me"];
};

export const useCurrentUser = ({ skip }: { skip?: boolean }): CurrentUser => {
  const { loading, error, data } = useCurrentUserQuery({
    skip,
    errorPolicy: "all",
  });

  const user = data && data.me;

  useEffect(() => {
    if (user) {
      updateOlarkFields(user);
    }
  }, [user]);

  return { loading, error, user };
};
