/** @jsx jsx */
import { useRouter } from "next/router";
import { useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, Grid, Heading, jsx, Select, Text } from "theme-ui";

import { useLoginState } from "~/app/profile/hooks";
import { Alert } from "~/components/alert";
import { Link } from "~/components/link";
import { LoginForm } from "~/components/login-form";
import { MetaTags } from "~/components/meta-tags";
import { SubmissionAccordion } from "~/components/submission-accordion";
import { useVotingSubmissionsQuery } from "~/types";

import { TagsFilter } from "./tags-filter";

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

const getAsArray = (value: string | string[]): string[] => {
  if (!value) {
    return [];
  }

  return Array.isArray(value) ? value : [value];
};

export const VotingPage: React.SFC = () => {
  const [loggedIn] = useLoginState();
  const [votedSubmissions, setVotedSubmissions] = useState(new Set());
  const router = useRouter();

  const [filters, { select, raw }] = useFormState<Filters>(
    {
      vote: (router.query.vote as VoteTypes) ?? "all",
      language: (router.query.language as string) ?? "",
      topic: (router.query.topic as string) ?? "",
      tags: getAsArray(router.query.tags),
    },
    {
      onChange(e, stateValues, nextStateValues) {
        setVotedSubmissions(new Set());

        const qs = new URLSearchParams();
        const keys = Object.keys(nextStateValues) as (keyof Filters)[];

        keys.forEach((key) => {
          const value = nextStateValues[key];

          if (Array.isArray(value)) {
            value.forEach((item) => qs.append(key, item));
          } else if (value) {
            qs.append(key, value);
          }
        });

        const currentPath = router.pathname.replace(
          "[lang]",
          router.query.lang as string,
        );

        router.replace("/[lang]/voting", `${currentPath}?${qs.toString()}`);
      },
    },
  );

  const { loading, error, data } = useVotingSubmissionsQuery({
    variables: {
      conference: process.env.conferenceCode,
    },
    errorPolicy: "all",
    skip: !loggedIn,
  });

  const onVote = useCallback(
    (submission) =>
      setVotedSubmissions((submissions) => submissions.add(submission.id)),
    [],
  );

  const cannotVoteErrors =
    error &&
    error.graphQLErrors.findIndex(
      (e) => e.message === "You need to have a ticket to see submissions",
    ) !== -1;

  const isVotingClosed = data && !data.conference.isVotingOpen;

  return (
    <Box>
      <FormattedMessage id="voting.seoTitle">
        {(title) => <MetaTags title={title} />}
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
            gap={4}
            sx={{
              gridTemplateColumns: [null, "1fr 1fr"],
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

            {!isVotingClosed && (
              <Grid
                sx={{
                  gridTemplateColumns: [null, null, "1fr 1fr"],
                  gridTemplateRows: [
                    "repeat(4, 46px)",
                    null,
                    "repeat(2, 46px)",
                  ],
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
                    {(text) => <option value="">{text}</option>}
                  </FormattedMessage>
                  {data?.conference.topics.map((topic) => (
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
                    {(text) => <option value="">{text}</option>}
                  </FormattedMessage>
                  {data?.conference.languages.map((language) => (
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
                    {(text) => <option value="all">{text}</option>}
                  </FormattedMessage>
                  <FormattedMessage id="voting.notVoted">
                    {(text) => <option value="notVoted">{text}</option>}
                  </FormattedMessage>
                  <FormattedMessage id="voting.votedOnly">
                    {(text) => <option value="votedOnly">{text}</option>}
                  </FormattedMessage>
                </Select>

                <TagsFilter
                  {...raw("tags")}
                  tags={data?.submissionTags ?? []}
                />
              </Grid>
            )}
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
              <Link path="/[lang]/tickets">
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

      {isVotingClosed && (
        <Box sx={{ borderTop: "primary" }}>
          <Grid
            sx={{
              maxWidth: "container",
              mx: "auto",
              mt: 3,
              px: 3,
              mb: [5, 5, 0],
              gridTemplateColumns: ["1fr", "0.5fr"],
            }}
          >
            <Heading sx={{ mb: 3 }}>
              <FormattedMessage id="voting.closed.heading" />
            </Heading>
            <Text>
              <FormattedMessage
                id="voting.closed.body"
                values={{
                  twitter: (
                    <a target="_blank" href="https://twitter.com/pyconit">
                      Twitter
                    </a>
                  ),
                }}
              />
            </Text>
          </Grid>
        </Box>
      )}

      {!loggedIn && (
        <Box sx={{ borderTop: "primary", mb: 5 }}>
          <Box
            sx={{
              maxWidth: "container",
              mx: "auto",
              mt: 3,
              px: [3, 3, 3, 0],
            }}
          >
            <Alert variant="info">
              <FormattedMessage id="voting.needToBeLoggedIn" />
            </Alert>
          </Box>
          <LoginForm
            next={process.browser ? window.location?.pathname : null}
          />
        </Box>
      )}

      {loggedIn && !isVotingClosed && data?.conference.submissions && (
        <Box
          as="ul"
          sx={{
            listStyle: "none",
          }}
        >
          {data.conference.submissions
            .filter((submission) => {
              if (
                filters.values.topic &&
                submission.topic?.id !== filters.values.topic
              ) {
                return false;
              }

              if (
                filters.values.language &&
                submission.languages?.findIndex(
                  (language) => language.code === filters.values.language,
                ) === -1
              ) {
                return false;
              }

              if (
                filters.values.tags.length > 0 &&
                submission.tags?.every(
                  (st) => filters.values.tags.indexOf(st.id) === -1,
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

export default VotingPage;
