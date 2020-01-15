/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Heading, Text } from "@theme-ui/components";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "../../app/profile/hooks";
import { useConference } from "../../context/conference";
import {
  VotingSubmissionsQuery,
  VotingSubmissionsQueryVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { Link } from "../link";
import { LoginForm } from "../login-form";
import { MetaTags } from "../meta-tags";
import { SubmissionAccordion } from "./submission-accordion";
import VOTING_SUBMISSIONS from "./voting-submissions.graphql";

type Props = RouteComponentProps & {
  lang: string;
};

export const VotingPage: React.SFC<Props> = ({ location }) => {
  const [loggedIn] = useLoginState();

  const { code: conferenceCode } = useConference();
  const { loading, error, data } = useQuery<
    VotingSubmissionsQuery,
    VotingSubmissionsQueryVariables
  >(VOTING_SUBMISSIONS, {
    variables: {
      conference: conferenceCode,
    },
    skip: !loggedIn,
  });

  const cannotVoteErrors =
    error?.graphQLErrors.findIndex(
      e => e.message === "You can't see details for this submission",
    ) !== -1;

  return (
    <Box>
      <FormattedMessage id="voting.seoTitle">
        {title => <MetaTags title={title} />}
      </FormattedMessage>

      <Box
        sx={{
          borderBottom: loggedIn ? "" : "primary",
        }}
      >
        <Box
          sx={{
            maxWidth: "container",
            mx: "auto",
            px: 3,
          }}
        >
          <Box
            sx={{
              maxWidth: 500,
            }}
          >
            <Heading>
              <FormattedMessage id="voting.heading" />
            </Heading>
            <Text my={4}>
              <FormattedMessage id="voting.introduction" />
            </Text>
          </Box>

          {!cannotVoteErrors && error && (
            <Alert variant="alert">{error.message}</Alert>
          )}

          {cannotVoteErrors && error && (
            <Alert variant="alert">
              <Link href="/:language/tickets">
                <FormattedMessage id="voting.buyTicketToVote" />
              </Link>
            </Alert>
          )}
          {loading && (
            <Alert variant="info">
              <FormattedMessage id="voting.loading" />
            </Alert>
          )}
        </Box>
      </Box>

      {!loggedIn && (
        <Fragment>
          <Box
            sx={{
              maxWidth: "container",
              mx: "auto",
              mt: 3,
            }}
          >
            <Alert variant="info">
              <FormattedMessage id="voting.needToBeLoggedIn" />
            </Alert>
          </Box>
          <LoginForm next={location?.href} />
        </Fragment>
      )}

      {loggedIn && data && (
        <Box
          as="ul"
          sx={{
            listStyle: "none",
          }}
        >
          {data.conference.submissions.map(submission => (
            <SubmissionAccordion
              vote={submission.myVote}
              key={submission.id}
              submission={submission}
            />
          ))}
        </Box>
      )}
    </Box>
  );
};
