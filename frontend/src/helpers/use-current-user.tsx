import { CurrentUserQueryResult, useCurrentUserQuery } from "~/types";

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

  const user = data?.me;

  return { loading, error, user };
};
