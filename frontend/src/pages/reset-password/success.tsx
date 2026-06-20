import type { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { DEFAULT_LOCALE } from "~/locale/languages";

export const getStaticProps: GetStaticProps = async () => {
  const client = getApolloClient();

  await prefetchSharedQueries(client, DEFAULT_LOCALE);

  return addApolloState(client, {
    props: {},
  });
};

export { RequestResetPasswordSuccessPageHandler as default } from "~/components/request-reset-password-success-page-handler";
