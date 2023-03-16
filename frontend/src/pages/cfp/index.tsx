/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Container, Heading, jsx, Text } from "theme-ui";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { Introduction } from "~/components/cfp-introduction";
import { CfpSendSubmission } from "~/components/cfp-send-submission";
import { Link } from "~/components/link";
import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  queryCfpForm,
  queryIsCfpOpen,
  queryTags,
  useIsCfpOpenQuery,
} from "~/types";

const CfpSectionOrClosedMessage = ({ open }: { open: boolean }) => {
  if (open) {
    return (
      <Fragment>
        <CfpSendSubmission />
      </Fragment>
    );
  }

  return (
    <Box sx={{ mt: 4, width: [null, null, "50%"] }}>
      <Heading sx={{ mb: 3 }}>
        <FormattedMessage id="cfp.closed.title" />
      </Heading>

      <Text sx={{ mb: 3 }}>
        <FormattedMessage id="cfp.closed.description" />
      </Text>

      <Text>
        <FormattedMessage id="cfp.closed.voting" />{" "}
        <Link path="/tickets">
          <FormattedMessage id="cfp.closed.buyTicket" />
        </Link>
      </Text>
    </Box>
  );
};

export const CFPPage = () => {
  const [isLoggedIn, _] = useLoginState();

  const code = process.env.conferenceCode;

  const { loading, data } = useIsCfpOpenQuery({
    variables: { conference: code },
  });

  return (
    <Fragment>
      <FormattedMessage id="cfp.pageTitle">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>
      <Introduction
        deadline={
          data?.conference.isCFPOpen
            ? data?.conference.cfpDeadline?.end
            : undefined
        }
      />

      <Box sx={{ px: 3 }}>
        <Container sx={{ maxWidth: "container", p: 0 }}>
          {isLoggedIn ? (
            !loading && (
              <CfpSectionOrClosedMessage
                open={data?.conference.isCFPOpen || false}
              />
            )
          ) : (
            <Fragment>
              <Alert variant="info" sx={{ mt: 4 }}>
                <FormattedMessage id="cfp.needToBeLoggedIn" />
              </Alert>
            </Fragment>
          )}
        </Container>
      </Box>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryIsCfpOpen(client, {
      conference: process.env.conferenceCode,
    }),
    queryCfpForm(client, {
      conference: process.env.conferenceCode,
    }),
    queryTags(client),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default CFPPage;
