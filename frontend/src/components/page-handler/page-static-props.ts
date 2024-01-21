import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { blocksDataFetching } from "~/components/blocks-renderer";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  PagePreviewQuery,
  PageQuery,
  queryPage,
  queryPagePreview,
} from "~/types";

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

  const [_, pageDataQuery] = await Promise.all([
    prefetchSharedQueries(client, locale),
    !preview
      ? queryPage(client, {
          language: locale,
          hostname: process.env.cmsHostname,
          slug: process.env.conferenceCode,
        })
      : queryPagePreview(client, {
          contentType: previewData?.contentType,
          token: previewData?.token,
        }),
  ]);

  const pageData = preview
    ? (pageDataQuery.data as PagePreviewQuery).pagePreview
    : (pageDataQuery.data as PageQuery).cmsPage;
  if (!pageData || pageData.__typename === "SiteNotFoundError") {
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
