import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  queryIndexPage,
  queryInformationSection,
  queryKeynotesSection,
  queryMapWithLink,
} from "~/types";

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryKeynotesSection(client, {
      code: process.env.conferenceCode,
      language: locale,
    }),
    queryMapWithLink(client, {
      code: process.env.conferenceCode,
    }),
    queryIndexPage(client, {
      language: locale,
      code: process.env.conferenceCode,
    }),
    queryInformationSection(client, {
      code: process.env.conferenceCode,
    }),
  ]);

  const utcHours = new Date().getUTCHours();
  const cycle = utcHours > 5 && utcHours < 17 ? "day" : "night";

  return addApolloState(client, {
    props: {
      cycle,
    },
  });
};

export { HomePagePageHandler as default } from "~/components/homepage-page-handler";
