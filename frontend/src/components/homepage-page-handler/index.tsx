import { Page } from "@python-italia/pycon-styleguide";
import React, { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import { MetaTags } from "~/components/meta-tags";
import { useCurrentLanguage } from "~/locale/context";
import { GenericPage, useIndexPageQuery } from "~/types";

import { BlocksRenderer } from "../blocks-renderer";

export const HomePagePageHandler = ({ blocksProps }) => {
  const language = useCurrentLanguage();
  const {
    data: { cmsPage },
  } = useIndexPageQuery({
    variables: {
      hostname: process.env.cmsHostname,
      code: process.env.conferenceCode,
      language,
    },
  });

  if (!cmsPage) {
    return null;
  }

  return (
    <Fragment>
      <FormattedMessage id="home.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Page startSeparator={false}>
        <BlocksRenderer
          blocksProps={blocksProps}
          blocks={(cmsPage as GenericPage).body}
        />
      </Page>
    </Fragment>
  );
};
