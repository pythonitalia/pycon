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

export { ResetPasswordSuccessPageHandler as default } from "~/components/reset-password-success-page-handler";
