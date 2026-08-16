import type { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryAllJobListings } from "~/types";

export const getStaticProps: GetStaticProps = async () => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client),
    queryAllJobListings(client, {
      conference: process.env.conferenceCode,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export { JobPageHandler as default } from "~/components/job-page-handler";
