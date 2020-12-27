import { useCurrentUserQuery } from "~/types";

export const useCurrentUser = ({ skip }: { skip?: boolean }) => {
  const { loading, error, data } = useCurrentUserQuery({
    skip,
    errorPolicy: "all",
  });

  const user = data && data.me;

  return { loading, error, user };
};
