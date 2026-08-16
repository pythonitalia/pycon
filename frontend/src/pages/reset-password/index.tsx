import type { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";

export const getStaticProps: GetStaticProps = async () => {
  const client = getApolloClient();

  await prefetchSharedQueries(client);

  return addApolloState(client, {
    props: {},
  });
};

export { RequestResetPasswordPageHandler as default } from "~/components/request-reset-password-page-handler";
