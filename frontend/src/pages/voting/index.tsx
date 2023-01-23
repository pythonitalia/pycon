/** @jsxRuntime classic */

/** @jsx jsx */
import {
  MultiplePartsCardCollection,
  Heading,
  Section,
  Grid,
  Text,
  Page,
  Link,
  BasicButton,
  Spacer,
  CardPart,
  MultiplePartsCard,
  Button,
  HorizontalStack,
} from "@python-italia/pycon-styleguide";
import React, { useEffect, useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx, Select } from "theme-ui";

import { GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { MetaTags } from "~/components/meta-tags";
import { TagsFilter } from "~/components/tags-filter";
import { VotingCard } from "~/components/voting-card";
import { formatDeadlineDateTime } from "~/helpers/deadlines";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useInfiniteFetchScroll } from "~/helpers/use-infinite-fetch-scroll";
import { useCurrentLanguage } from "~/locale/context";
import { useVotingSubmissionsQuery } from "~/types";

type VoteTypes = "all" | "votedOnly" | "notVoted";

type Filters = {
  language: string;
  vote: VoteTypes;
  tags: string[];
};

const getAsArray = (value: string | string[]): string[] => {
  if (!value) {
    return [];
  }

  return Array.isArray(value) ? value : [value];
};

export const VotingPage = () => {
  const [votedSubmissions, setVotedSubmissions] = useState(new Set());
  const router = useRouter();
  const language = useCurrentLanguage();

  const [filters, { select, raw }] = useFormState<Filters>(
    {},
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

        const currentPath = router.pathname;
        router.replace("/voting", `${currentPath}?${qs.toString()}`);
      },
    },
  );

  useEffect(() => {
    if (!router.isReady) {
      return;
    }

    filters.setField("vote", (router.query.vote as VoteTypes) ?? "all");
    filters.setField("language", (router.query.language as string) ?? "");
    filters.setField("tags", getAsArray(router.query.tags));
  }, [router.isReady]);

  const duplicateSubmissionsHotfix = new Set();

  const filterVisibleSubmissions = (submission) => {
    if (duplicateSubmissionsHotfix.has(submission.id)) {
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
      submission.tags?.every((st) => filters.values.tags.indexOf(st.id) === -1)
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

    if (voteStatusFilter === "votedOnly" && submission.myVote === null) {
      return false;
    }

    duplicateSubmissionsHotfix.add(submission.id);
    return true;
  };

  const { loading, error, data, fetchMore } = useVotingSubmissionsQuery({
    variables: {
      conference: process.env.conferenceCode,
      loadMore: false,
      language,
    },
    errorPolicy: "all",
  });

  const onVote = useCallback(
    (submission) =>
      setVotedSubmissions((submissions) => submissions.add(submission.id)),
    [],
  );

  const { isFetchingMore, hasMore, forceLoadMore } = useInfiniteFetchScroll({
    fetchMore,
    after:
      data && data.submissions && data.submissions.length > 0
        ? (data.submissions[data.submissions.length - 1]?.id as any)
        : undefined,
    hasMoreResultsCallback(newData) {
      return newData && newData.submissions && newData.submissions.length > 0;
    },
    shouldFetchAgain(newData) {
      if (!newData || newData.submissions === null) {
        return null;
      }

      if (newData.submissions.filter(filterVisibleSubmissions).length === 0) {
        return newData.submissions.length > 0
          ? newData.submissions[newData.submissions.length - 1].id
          : null;
      }

      return null;
    },
  });

  const cannotVoteErrors =
    error &&
    error.graphQLErrors.findIndex(
      (e) => e.message === "You need to have a ticket to see submissions",
    ) !== -1;

  const isVotingClosed = data && !data?.conference?.isVotingOpen;
  const userCannotVote =
    loading || (cannotVoteErrors ?? false) || (error ?? false);
  const showFilters = !isVotingClosed && !userCannotVote;
  const votingDeadline = data?.conference?.isVotingOpen
    ? data?.conference.votingDeadline?.end
    : undefined;

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="voting.seoTitle">
        {(title) => <MetaTags title={title} />}
      </FormattedMessage>

      <Section>
        <Heading size="display1">
          <FormattedMessage id="voting.heading" />
        </Heading>
        <Spacer size="large" />

        <Text as="p" size={2}>
          <FormattedMessage id="voting.introduction" />
        </Text>
        {votingDeadline && (
          <Text as="p" size={2}>
            <FormattedMessage
              id="voting.introductionDeadline"
              values={{
                deadline: (
                  <Text size={2} weight="strong">
                    {formatDeadlineDateTime(votingDeadline, language)}
                  </Text>
                ),
              }}
            />
          </Text>
        )}
        <Spacer size="small" />
        <BasicButton href="/voting-info">
          <FormattedMessage id="global.learnMore" />
        </BasicButton>
        <Spacer size="large" />

        {showFilters && (
          <Grid cols={2}>
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

            <TagsFilter {...raw("tags")} tags={data?.votingTags ?? []} />
          </Grid>
        )}
      </Section>

      <Section>
        {userCannotVote && (
          <>
            {!cannotVoteErrors && error && (
              <Alert variant="alert">{error.message}</Alert>
            )}

            {cannotVoteErrors && error && (
              <>
                <Heading>
                  <FormattedMessage id="voting.errors.cannotVote.heading" />
                </Heading>

                <Text>
                  <FormattedMessage
                    id="voting.errors.cannotVote.body"
                    values={{
                      linkVotingInfo: (
                        <Link href="/voting-info">
                          <FormattedMessage id="voting.errors.cannotVote.linkVotingInfo.text" />
                        </Link>
                      ),
                      linkTicket: (
                        <Link href="/tickets">
                          <FormattedMessage id="voting.errors.cannotVote.linkTicket.text" />
                        </Link>
                      ),
                    }}
                  />
                </Text>
              </>
            )}

            {loading && (
              <HorizontalStack alignItems="center" justifyContent="center">
                <Text as="p" size={2}>
                  <FormattedMessage id="voting.loading" />
                </Text>
              </HorizontalStack>
            )}
          </>
        )}

        {isVotingClosed && (
          <>
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
          </>
        )}

        {!isVotingClosed && data?.submissions && (
          <>
            <MultiplePartsCardCollection>
              <MultiplePartsCard>
                <CardPart contentAlign="left">
                  <Heading size={2}>
                    <FormattedMessage id="voting.proposals" />
                  </Heading>
                </CardPart>
              </MultiplePartsCard>
              {data.submissions
                .filter(filterVisibleSubmissions)
                .map((submission) => (
                  <VotingCard
                    key={submission.id}
                    submission={submission}
                    onVote={onVote}
                  />
                ))}
            </MultiplePartsCardCollection>
          </>
        )}
        <Spacer size="xl" />

        <HorizontalStack alignItems="center" justifyContent="center">
          {!isVotingClosed && data?.submissions && (
            <>
              {isFetchingMore && (
                <Text as="p" size={2}>
                  <FormattedMessage id="voting.loading" />
                </Text>
              )}

              {hasMore && !loading && !isFetchingMore && (
                <Button onClick={forceLoadMore} role="secondary" size="small">
                  <FormattedMessage id="global.loadMore" />
                </Button>
              )}
            </>
          )}
        </HorizontalStack>
      </Section>
    </Page>
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
