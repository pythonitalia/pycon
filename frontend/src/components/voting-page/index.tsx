/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { navigate, RouteComponentProps } from "@reach/router";
import { Box, Flex, Grid, Heading, Select, Text } from "@theme-ui/components";
import { Fragment, useCallback, useEffect, useState } from "react";
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
import { TagsFilter } from "./tags-filter";
import VOTING_SUBMISSIONS from "./voting-submissions.graphql";

type VoteTypes = "all" | "votedOnly" | "notVoted";

type Filters = {
  topic: string;
  language: string;
  vote: VoteTypes;
  tags: string[];
};

const COLORS = [
  {
    background: "blue",
    heading: "white",
  },
  {
    background: "lightBlue",
    heading: "black",
  },
];

export const VotingPage: React.SFC<RouteComponentProps> = ({ location }) => {
  const [loggedIn] = useLoginState();
  const [votedSubmissions, setVotedSubmissions] = useState(new Set());

  const currentQs = new URLSearchParams(location?.search);

  const [filters, { select, raw }] = useFormState<Filters>(
    {
      vote: (currentQs.get("vote") as VoteTypes) ?? "all",
      language: currentQs.get("language") ?? "",
      topic: currentQs.get("topic") ?? "",
      tags: currentQs.getAll("tags"),
    },
    {
      onChange(e, stateValues, nextStateValues) {
        setVotedSubmissions(new Set());

        if (!location) {
          return;
        }

        const qs = new URLSearchParams();
        const keys = Object.keys(nextStateValues) as (keyof Filters)[];

        keys.forEach(key => {
          const value = nextStateValues[key];

          if (Array.isArray(value)) {
            value.forEach(item => qs.append(key, item));
          } else if (value) {
            qs.append(key, value);
          }
        });

        navigate(`${location.pathname}?${qs.toString()}`, {
          replace: true,
        });
      },
    },
  );

  const { code: conferenceCode } = useConference();
  const { loading, error, data } = useQuery<
    VotingSubmissionsQuery,
    VotingSubmissionsQueryVariables
  >(VOTING_SUBMISSIONS, {
    variables: {
      conference: conferenceCode,
    },
    errorPolicy: "all",
    skip: !loggedIn,
  });

  const onVote = useCallback(
    submission =>
      setVotedSubmissions(submissions => submissions.add(submission.id)),
    [],
  );

  const cannotVoteErrors =
    error &&
    error.graphQLErrors.findIndex(
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
            </Box>

            <Grid
              sx={{
                gridTemplateColumns: [null, null, "1fr 1fr"],
                gridTemplateRows: ["repeat(46px, 4)", null, "repeat(46px, 2)"],
                mb: 4,
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

              <TagsFilter {...raw("tags")} tags={data?.submissionTags ?? []} />
            </Grid>
          </Grid>
        </Box>
      </Box>

      {loggedIn && (loading || cannotVoteErrors || error) && (
        <Box
          sx={{
            maxWidth: "container",
            mx: "auto",
            px: 3,
          }}
        >
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
      )}

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

      {cannotVoteErrors && (
        <Box
          sx={{
            maxWidth: "container",
            mx: "auto",
            mt: 3,
            px: 3,
          }}
        >
          <Alert variant="alert">
            <Link href="/:language/tickets">
              <FormattedMessage id="voting.buyTicketToVote" />
            </Link>
          </Alert>
        </Box>
      )}

      {loggedIn && data?.conference.submissions && (
        <Box
          as="ul"
          sx={{
            listStyle: "none",
          }}
        >
          {data.conference.submissions
            .filter(submission => {
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

              if (
                filters.values.tags.length > 0 &&
                submission.tags?.every(
                  st => filters.values.tags.indexOf(st.id) === -1,
                )
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
                backgroundColor={COLORS[index % COLORS.length].background}
                headingColor={COLORS[index % COLORS.length].heading}
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
