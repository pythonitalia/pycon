/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { GrantForm } from "~/components/grant-form";
import { Introduction } from "~/components/grants-introduction";
import { MetaTags } from "~/components/meta-tags";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryGrantDeadline, useGrantDeadlineQuery } from "~/types";

export const GrantsPage = () => {
  const code = process.env.conferenceCode;
  const {
    data: {
      conference: {
        deadline
      }
    },
  } = useGrantDeadlineQuery({
    variables: {
      conference: code,
    }
  })

  console.log("deadline", deadline)

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

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryGrantDeadline(client, {
      conference: process.env.conferenceCode
    })
  ])

  return addApolloState(client, {
    props: {},
  });
};

export default GrantsPage;
