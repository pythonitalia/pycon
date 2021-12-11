/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx, Text } from "theme-ui";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { GrantForm } from "~/components/grant-form";
import { Introduction } from "~/components/grants-introduction";
import { MetaTags } from "~/components/meta-tags";
import { formatDeadlineDateTime } from "~/helpers/deadlines";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { Language } from "~/locale/languages";
import {
  DeadlineStatus,
  queryGrantDeadline,
  useGrantDeadlineQuery,
} from "~/types";

import ErrorPage from "../_error";

const GrantsComingSoon = ({ start }: { start: string }) => {
  const language = useCurrentLanguage();

  return (
    <Box>
      <Text>
        <FormattedMessage
          id="grants.comingSoon"
          values={{
            start: (
              <Text as="span" sx={{ fontWeight: "bold" }}>
                {formatDeadlineDateTime(start, language)}
              </Text>
            ),
          }}
        />
      </Text>
    </Box>
  );
};

const GrantsClosed = () => {
  return (
    <Box>
      <Text>
        <FormattedMessage id="grants.closed" />
      </Text>
    </Box>
  );
};

export const GrantsPage = () => {
  const code = process.env.conferenceCode;
  const {
    data: {
      conference: { deadline },
    },
  } = useGrantDeadlineQuery({
    variables: {
      conference: code,
    },
  });

  if (!deadline) {
    return <ErrorPage statusCode={404} />;
  }

  const { status, start, end } = deadline;

  return (
    <React.Fragment>
      <FormattedMessage id="grants.pageTitle">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Introduction end={status === DeadlineStatus.HappeningNow ? end : null} />

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
          my: 5,
        }}
      >
        {status === DeadlineStatus.HappeningNow && (
          <GrantForm conference={code} />
        )}
        {status === DeadlineStatus.InTheFuture && (
          <GrantsComingSoon start={start} />
        )}
        {status === DeadlineStatus.InThePast && <GrantsClosed />}
      </Box>
    </React.Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryGrantDeadline(client, {
      conference: process.env.conferenceCode,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default GrantsPage;
