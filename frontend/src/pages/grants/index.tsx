/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx, Text } from "theme-ui";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { GrantForm } from "~/components/grant-form";
import { Introduction } from "~/components/grants-introduction";
import { LoginForm } from "~/components/login-form";
import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { formatDeadlineDateTime } from "~/helpers/deadlines";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
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
  const [isLoggedIn, _] = useLoginState();
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
        {isLoggedIn ? (
          <>
            {" "}
            {status === DeadlineStatus.HappeningNow && (
              <GrantForm conference={code} />
            )}
            {status === DeadlineStatus.InTheFuture && (
              <GrantsComingSoon start={start} />
            )}
            {status === DeadlineStatus.InThePast && <GrantsClosed />}
          </>
        ) : (
          <>
            <Alert variant="info" sx={{ mt: 4 }}>
              <FormattedMessage id="grants.form.needToBeLoggedIn" />
            </Alert>

            <LoginForm
              sx={{ mt: 4 }}
              next={
                typeof window !== "undefined" ? window.location?.pathname : null
              }
            />
          </>
        )}
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
