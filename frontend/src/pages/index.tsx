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
      hostname: process.env.cmsHostname,
      code: process.env.conferenceCode,
    }),
  ]);

  if (!pageQuery.data.cmsPage) {
    return {
      notFound: true,
    };
  }

  const { dataFetching, staticProps } = blocksDataFetching(
    client,
    (pageQuery.data.cmsPage as GenericPage).body,
    locale,
  );

  await dataFetching;

  return addApolloState(client, {
    props: {
      blocksProps: staticProps,
    },
  });
};

export { HomePagePageHandler as default } from "~/components/homepage-page-handler";
