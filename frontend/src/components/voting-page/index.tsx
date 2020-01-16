/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Flex, Grid, Heading, Select, Text } from "@theme-ui/components";
import { Fragment, useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
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

type Filters = {
  topic: string;
  language: string;
  vote: "all" | "votedOnly" | "notVoted";
};

const COLORS = ["blue", "keppel", "orange", "yellow"];

export const VotingPage: React.SFC<RouteComponentProps> = ({ location }) => {
  const [loggedIn] = useLoginState();
  const [filters, { select }] = useFormState<Filters>({ vote: "all" });
  const [votedSubmissions, setVotedSubmissions] = useState(new Set());

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

  const onVote = useCallback(
    submission =>
      setVotedSubmissions(submissions => submissions.add(submission.id)),
    [],
  );

  const cannotVoteErrors =
    error?.graphQLErrors.findIndex(
      e => e.message === "You need to have a ticket to see submissions",
    ) !== -1;

  return (
    <Box>
      <FormattedMessage id="voting.seoTitle">
        {title => <MetaTags title={title} />}
      </FormattedMessage>

      <Box>
        <Box
          sx={{
            maxWidth: "container",
            mx: "auto",
            px: 3,
          }}
        >
          <Grid
            sx={{
              gridTemplateColumns: [null, "1fr 1fr"],
              gridColumnGap: 4,
            }}
          >
            <Box>
              <Heading>
                <FormattedMessage id="voting.heading" />
              </Heading>

              <Text my={4}>
                <FormattedMessage id="voting.introduction" />
              </Text>

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
            <Flex
              sx={{
                flexDirection: ["column", "row"],
                alignItems: [null, "flex-end"],
                justifyContent: [null, "flex-end"],
                mb: 4,

                "div + div": {
                  select: {
                    borderLeft: [null, "none"],
                  },
                },
              }}
            >
              <Select
                {...select("topic")}
                sx={{
                  background: "orange",
                  borderRadius: 0,
                }}
              >
                <FormattedMessage id="voting.allTopics">
                  {text => <option value="">{text}</option>}
                </FormattedMessage>
                {data?.conference.topics.map(topic => (
                  <option key={topic.id} value={topic.id}>
                    {topic.name}
                  </option>
                ))}
              </Select>

              <Select
                {...select("language")}
                sx={{
                  background: "violet",
                  mt: [3, 0],
                  borderRadius: 0,
                }}
              >
                <FormattedMessage id="voting.allLanguages">
                  {text => <option value="">{text}</option>}
                </FormattedMessage>
                {data?.conference.languages.map(language => (
                  <option key={language.id} value={language.code}>
                    {language.name}
                  </option>
                ))}
              </Select>

              <Select
                {...select("vote")}
                sx={{
                  background: "keppel",
                  mt: [3, 0],
                  borderRadius: 0,
                }}
              >
                <FormattedMessage id="voting.allSubmissions">
                  {text => <option value="all">{text}</option>}
                </FormattedMessage>
                <FormattedMessage id="voting.notVoted">
                  {text => <option value="notVoted">{text}</option>}
                </FormattedMessage>
                <FormattedMessage id="voting.votedOnly">
                  {text => <option value="votedOnly">{text}</option>}
                </FormattedMessage>
              </Select>
            </Flex>
          </Grid>
        </Box>
      </Box>

      {!loggedIn && (
        <Box sx={{ borderTop: "primary" }}>
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
        </Box>
      )}

      {loggedIn && data && (
        <Box
          as="ul"
          sx={{
            listStyle: "none",
          }}
        >
          {data.conference
            .submissions!.filter(submission => {
              if (
                filters.values.topic &&
                submission.topic?.id !== filters.values.topic
              ) {
                return false;
              }

              if (
                filters.values.language &&
                submission.languages?.findIndex(
                  language => language.code === filters.values.language,
                ) === -1
              ) {
                return false;
              }

              const voteStatusFilter = filters.values.vote;

              if (
                voteStatusFilter === "notVoted" &&
                submission.myVote !== null &&
                !votedSubmissions.has(submission.id)
              ) {
                return false;
              }

              if (
                voteStatusFilter === "votedOnly" &&
                submission.myVote === null
              ) {
                return false;
              }

              return true;
            })
            .map((submission, index) => (
              <SubmissionAccordion
                color={COLORS[index % COLORS.length]}
                vote={submission.myVote}
                key={submission.id}
                submission={submission}
                onVote={onVote}
              />
            ))}
        </Box>
      )}
    </Box>
  );
};
