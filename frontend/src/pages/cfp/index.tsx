/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment, useMemo } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Container, Heading, jsx, Text } from "theme-ui";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { Introduction } from "~/components/cfp-introduction";
import { CfpSendSubmission } from "~/components/cfp-send-submission";
import { Link } from "~/components/link";
import { LoginForm } from "~/components/login-form";
import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { MySubmissions } from "~/components/profile/my-submissions";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { formatDeadlineDate } from "~/helpers/deadlines";
import {
  queryCfpForm,
  queryIsCfpOpen,
  queryTags,
  useIsCfpOpenQuery,
} from "~/types";
import { useCurrentLanguage } from "~/locale/context";

const CfpSectionOrClosedMessage: React.SFC<{ open: boolean }> = ({ open }) => {
  if (open) {
    return (
      <Fragment>
        <MySubmissions sx={{ mb: 4 }} />
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

export const CFPPage: React.SFC = () => {
  const [isLoggedIn, _] = useLoginState();
  const language = useCurrentLanguage();

  const code = process.env.conferenceCode;

  const { loading, data } = useIsCfpOpenQuery({
    variables: { conference: code },
  });

  const cfpDeadline = useMemo(() => {
    return data?.conference.deadlines.filter(
      (deadline) => deadline.type === "cfp",
    )[0].end;
  }, data);

  return (
    <Fragment>
      <FormattedMessage id="cfp.pageTitle">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>
      <Introduction deadline={formatDeadlineDate(cfpDeadline, language)} />

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

              <LoginForm
                sx={{ mt: 4 }}
                next={
                  typeof window !== "undefined"
                    ? window.location?.pathname
                    : null
                }
              />
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
