import { Page as BasePage } from "@python-italia/pycon-styleguide";
import React, { Fragment } from "react";

import { BlocksRenderer } from "~/components/blocks-renderer";
import { MetaTags } from "~/components/meta-tags";
import { GenericPage } from "~/types";

import { usePageOrPreview } from "./use-page-or-preview";

export const PageHandler = ({ blocksProps, isPreview, previewData, slug }) => {
  const cmsPage = usePageOrPreview({
    slug,
    isPreview,
    previewData,
  });

  const page = cmsPage as GenericPage;

  return (
    <Fragment>
      <MetaTags title={page.title} description={page.searchDescription} />

      <BasePage endSeparator={false}>
        <BlocksRenderer blocks={page.body} blocksProps={blocksProps} />
      </BasePage>
    </Fragment>
  );
};
