import { Page as BasePage } from "@python-italia/pycon-styleguide";
import React, { Fragment } from "react";

import { BlocksRenderer } from "~/components/blocks-renderer";
import { MetaTags } from "~/components/meta-tags";

import { usePageOrPreview } from "./use-page-or-preview";

export const PageHandler = ({ blocksProps, isPreview, previewData, slug }) => {
  const page = usePageOrPreview({
    fetcher: "page",
    slug,
    isPreview,
    previewData,
  });

  return (
    <Fragment>
      <MetaTags title={page.title} description={page.searchDescription} />

      <BasePage endSeparator={false}>
        <BlocksRenderer blocks={page.body} blocksProps={blocksProps} />
      </BasePage>
    </Fragment>
  );
};
