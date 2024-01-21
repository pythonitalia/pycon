import { Page as BasePage } from "@python-italia/pycon-styleguide";
import React, { Fragment } from "react";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import {
  BlocksRenderer,
  blocksDataFetching,
} from "~/components/blocks-renderer";
import { MetaTags } from "~/components/meta-tags";
import { PageHandler } from "~/components/page-handler";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { GenericPage, queryAllPages, queryPage, usePageQuery } from "~/types";

export const FrontendPage = ({ blocksProps, isPreview, previewData }) => {
  const router = useRouter();
  const slug = router.query.slug as string;
  return (
    <PageHandler
      isPreview={isPreview}
      previewData={previewData}
      slug={slug}
      blocksProps={blocksProps}
    />
  );
};

export { getStaticProps } from "~/components/page-handler/page-static-props";

export const getStaticPaths: GetStaticPaths = async () => {
  const client = getApolloClient();
  const [
    {
      data: { cmsPages: italianPages },
    },
    {
      data: { cmsPages: englishPages },
    },
  ] = await Promise.all([
    queryAllPages(client, {
      hostname: process.env.cmsHostname,
      language: "it",
    }),
    queryAllPages(client, {
      hostname: process.env.cmsHostname,
      language: "en",
    }),
  ]);

  const paths = [
    ...italianPages.map((page) => ({
      params: {
        slug: page.slug,
      },
      locale: "it",
    })),
    ...englishPages.map((page) => ({
      params: {
        slug: page.slug,
      },
      locale: "en",
    })),
  ];

  return {
    paths,
    fallback: "blocking",
  };
};

export default FrontendPage;
