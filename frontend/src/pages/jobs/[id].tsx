import { GetStaticPaths, GetStaticProps } from "next";

import { getApolloClient, addApolloState } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryAllJobListings } from "~/types";

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryAllJobListings(client, {
      language: locale,
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
    data: { jobListings: italianJobListings },
  } = await queryAllJobListings(client, {
    language: "it",
    conference: process.env.conferenceCode,
  });
  const {
    data: { jobListings: englishJobListings },
  } = await queryAllJobListings(client, {
    language: "en",
    conference: process.env.conferenceCode,
  });

  const paths = [
    ...italianJobListings.map((page) => ({
      params: {
        id: page.id,
      },
      locale: "it",
    })),
    ...englishJobListings.map((page) => ({
      params: {
        id: page.id,
      },
      locale: "en",
    })),
  ];

  return {
    paths,
    fallback: "blocking",
  };
};

export { JobDetailPageHandler as default } from "~/components/job-detail-page-handler";
