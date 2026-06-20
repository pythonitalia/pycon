import React from "react";

import type { GetStaticPaths } from "next";
import { useRouter } from "next/router";

import { getApolloClient } from "~/apollo/client";
import { PageHandler } from "~/components/page-handler";
import { DEFAULT_LOCALE } from "~/locale/languages";
import { queryAllPages } from "~/types";

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
  const {
    data: { cmsPages },
  } = await queryAllPages(client, {
    hostname: process.env.cmsHostname,
    language: DEFAULT_LOCALE,
  });

  const paths = cmsPages.map((page) => ({
    params: {
      slug: page.slug,
    },
  }));

  return {
    paths,
    fallback: "blocking",
  };
};

export default FrontendPage;
