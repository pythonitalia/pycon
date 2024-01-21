import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { blocksDataFetching } from "~/components/blocks-renderer";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryPage, queryPagePreview } from "~/types";

export const getStaticProps: GetStaticProps = async ({
  preview,
  previewData,
  locale,
}: {
  preview: boolean;
  previewData: {
    contentType: string;
    token: string;
  };
  locale: string;
}) => {
  const client = getApolloClient();

  const [_, pageQuery, previewQuery] = await Promise.all([
    prefetchSharedQueries(client, locale),
    queryPage(client, {
      language: locale,
      hostname: process.env.cmsHostname,
      slug: process.env.conferenceCode,
    }),
    preview
      ? queryPagePreview(client, {
          contentType: previewData.contentType,
          token: previewData.token,
        })
      : Promise.resolve(null),
  ]);

  const pageData =
    previewQuery === null
      ? pageQuery.data.cmsPage
      : previewQuery.data.pagePreview;

  if (!pageData) {
    return {
      notFound: true,
    };
  }

  const { dataFetching, staticProps } = blocksDataFetching(
    client,
    pageData.body,
    locale,
  );

  await dataFetching;

  return addApolloState(client, {
    props: {
      blocksProps: staticProps,
      isPreview: preview || false,
      previewData: previewData || null,
    },
  });
};
