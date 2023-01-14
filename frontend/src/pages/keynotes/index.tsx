import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryKeynotesPage } from "~/types";

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryKeynotesPage(client, {
      conference: process.env.conferenceCode,
      language: locale,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export { KeynotesListPageHandler as default } from "~/components/keynotes-list-page-handler";
