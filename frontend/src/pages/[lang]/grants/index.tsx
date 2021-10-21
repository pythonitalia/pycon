/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";

import { addApolloState } from "~/apollo/client";
import { GrantForm } from "~/components/grant-form";
import { Introduction } from "~/components/grants-introduction";
import { MetaTags } from "~/components/meta-tags";
import { prefetchSharedQueries } from "~/helpers/prefetch";

export const GrantsPage = () => {
  const code = process.env.conferenceCode;

  return (
    <React.Fragment>
      <FormattedMessage id="grants.pageTitle">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Introduction />

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
          my: 5,
        }}
      >
        <GrantForm conference={code} />
      </Box>
    </React.Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const lang = params.lang as string;

  await prefetchSharedQueries(lang);

  return addApolloState({
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () =>
  Promise.resolve({
    paths: [],
    fallback: "blocking",
  });

export default GrantsPage;
