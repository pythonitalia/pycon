import type { GetStaticPaths, GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { DEFAULT_LOCALE } from "~/locale/languages";
import { queryAllJobListings } from "~/types";

export const getStaticProps: GetStaticProps = async () => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, DEFAULT_LOCALE),
    queryAllJobListings(client, {
      conference: process.env.conferenceCode,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () => {
  const client = getApolloClient();

  const {
    data: { jobListings },
  } = await queryAllJobListings(client, {
    conference: process.env.conferenceCode,
  });

  const paths = jobListings.map((page) => ({
    params: {
      id: page.id,
    },
  }));

  return {
    paths,
    fallback: "blocking",
  };
};

export { JobDetailPageHandler as default } from "~/components/job-detail-page-handler";
