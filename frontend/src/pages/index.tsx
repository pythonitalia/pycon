import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { blocksDataFetching } from "~/components/blocks-renderer";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { GenericPage, queryIndexPage } from "~/types";

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  const [_, pageQuery] = await Promise.all([
    prefetchSharedQueries(client, locale),
    queryIndexPage(client, {
      language: locale,
      code: process.env.conferenceCode,
    }),
  ]);

  await blocksDataFetching(
    client,
    (pageQuery.data.cmsPage as GenericPage).body,
    locale,
  );

  const utcHours = new Date().getUTCHours();
  const cycle = utcHours > 5 && utcHours < 17 ? "day" : "night";

  return addApolloState(client, {
    props: {
      cycle,
    },
  });
};

export { HomePagePageHandler as default } from "~/components/homepage-page-handler";
