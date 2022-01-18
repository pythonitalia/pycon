/** @jsxRuntime classic */

/** @jsx jsx */
import { useCallback, useState, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Flex, Box, Grid, Heading, jsx, Select, Text } from "theme-ui";

import { GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { AnimatedEmoji } from "~/components/animated-emoji";
import { Button } from "~/components/button/button";
import { Link } from "~/components/link";
import { LoginForm } from "~/components/login-form";
import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { SubmissionAccordion } from "~/components/submission-accordion";
import { TagsFilter } from "~/components/tags-filter";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useInfiniteFetchScroll } from "~/helpers/use-infinite-fetch-scroll";
import { useVotingSubmissionsQuery } from "~/types";

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

export const VotingPage = () => {
  const [loggedIn] = useLoginState();
  const router = useRouter();

  const [filters, { select, raw }] = useFormState<Filters>(
    {},
    {
      onChange(e, stateValues, nextStateValues) {
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

        const currentPath = router.pathname;
        router.replace("/voting", `${currentPath}?${qs.toString()}`);
      },
    },
  );

  useEffect(() => {
    if (!router.isReady) {
      return;
    }

    filters.setField("vote", router.query.vote ?? "all");
    filters.setField("language", router.query.language);
    filters.setField("topic", router.query.topic);
    filters.setField("tags", getAsArray(router.query.tags));
  }, [router.isReady]);

  console.log("filters", filters.values);

  const { loading, error, data, fetchMore } = useVotingSubmissionsQuery({
    variables: {
      conference: process.env.conferenceCode,
      loadMore: false,
      filter: {
        language: filters.values.language,
        vote: filters.values.vote,
        topic: filters.values.topic,
        tags: filters.values.tags,
      },
    },
    errorPolicy: "all",
    skip: !loggedIn,
  });

  const { isFetchingMore, hasMore, forceLoadMore } = useInfiniteFetchScroll({
    fetchMore,
    after: data?.submissions?.at?.(-1)?.id,
    hasMoreResultsCallback(newData) {
      return newData.submissions.length > 0;
    },
    filters: filters.values,
  });

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
              <Link path="/tickets">
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
                    <a
                      target="_blank"
                      href="https://twitter.com/pyconit"
                      rel="noreferrer"
                    >
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
            next={
              typeof window !== "undefined" ? window.location?.pathname : null
            }
          />
        </Box>
      )}

      {loggedIn && !isVotingClosed && data?.submissions && (
        <Box
          as="ul"
          sx={{
            listStyle: "none",
          }}
        >
          {data.submissions.map((submission, index) => (
            <SubmissionAccordion
              backgroundColor={COLORS[index % COLORS.length].background}
              headingColor={COLORS[index % COLORS.length].heading}
              vote={submission.myVote}
              key={submission.id}
              submission={submission}
            />
          ))}
        </Box>
      )}

      <Flex
        sx={{
          maxWidth: "container",
          mx: "auto",
          my: 5,
          px: [3, 3, 3, 0],
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {isFetchingMore && (
          <FormattedMessage
            id="global.button.loading"
            values={{
              emoji: <AnimatedEmoji play={true} />,
            }}
          />
        )}

        {hasMore && !loading && !isFetchingMore && (
          <Button onClick={forceLoadMore}>
            <FormattedMessage id="global.loadMore" />
          </Button>
        )}
      </Flex>
    </Box>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await prefetchSharedQueries(client, locale);

  return addApolloState(client, {
    props: {},
  });
};

export default VotingPage;
