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
import React, { useEffect } from "react";
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

type Filters = {
  language: string;
  vote: string;
  tags: string[];
  type: string;
  audienceLevel: string;
};

const getAsArray = (value: string | string[]): string[] => {
  if (!value) {
    return [];
  }

  return Array.isArray(value) ? value : [value];
};

const toBoolean = (value: string): boolean | null => {
  if (value) {
    switch (value) {
      case "false":
        return false;

      case "true":
        return true;

      case "undefined":
        return null;

      case "null":
        return null;
    }
  }
};

export const VotingPage = () => {
  const router = useRouter();
  const language = useCurrentLanguage();

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
            qs.append(key, value.toString());
          }
        });

        const currentPath = router.pathname;
        router.replace("/voting", `${currentPath}?${qs.toString()}`);

        refetch({
          conference: process.env.conferenceCode,
          loadMore: false,
          language: nextStateValues.language,
          voted: toBoolean(nextStateValues.vote),
          tags: nextStateValues.tags,
          type: nextStateValues.type,
          audienceLevel: nextStateValues.audienceLevel,
        });
      },
    },
  );

  useEffect(() => {
    if (!router.isReady) {
      return;
    }

    filters.setField("vote", router.query.vote as string);
    filters.setField("language", (router.query.language as string) ?? "");
    filters.setField("tags", getAsArray(router.query.tags));
    filters.setField("type", (router.query.type as string) ?? "");
    filters.setField(
      "audienceLevel",
      (router.query.audienceLevel as string) ?? "",
    );
  }, [router.isReady]);

  const { loading, error, data, refetch, fetchMore } =
    useVotingSubmissionsQuery({
      variables: {
        conference: process.env.conferenceCode,
        loadMore: false,
        language: filters.values.language,
        voted: toBoolean(filters.values.vote),
        tags: filters.values.tags,
        type: filters.values.type,
        audienceLevel: filters.values.audienceLevel,
      },
      errorPolicy: "all",
    });

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

      // if (newData.submissions.filter(filterVisibleSubmissions).length === 0) {
      //   return newData.submissions.length > 0
      //     ? newData.submissions[newData.submissions.length - 1].id
      //     : null;
      // }

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
            <Select {...select("language")}>
              <FormattedMessage id="voting.allLanguages">
                {(text) => <option value="">{text}</option>}
              </FormattedMessage>
              {data?.conference.languages.map((language) => (
                <option key={language.id} value={language.code}>
                  {language.name}
                </option>
              ))}
            </Select>

            <Select {...select("vote")}>
              <FormattedMessage id="voting.allSubmissions">
                {(text) => <option value={null}>{text}</option>}
              </FormattedMessage>
              <FormattedMessage id="voting.notVoted">
                {(text) => <option value="false">{text}</option>}
              </FormattedMessage>
              <FormattedMessage id="voting.votedOnly">
                {(text) => <option value="true">{text}</option>}
              </FormattedMessage>
            </Select>

            <TagsFilter {...raw("tags")} tags={data?.votingTags ?? []} />

            <Select {...select("audienceLevel")}>
              <FormattedMessage id="cfp.selectAudience">
                {(txt) => (
                  <option value="" disabled={true}>
                    {txt}
                  </option>
                )}
              </FormattedMessage>
              {data?.conference.audienceLevels.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name}
                </option>
              ))}
            </Select>

            <Select {...select("type")}>
              <FormattedMessage id="cfp.choosetype">
                {(txt) => (
                  <option value="" disabled={true}>
                    {txt}
                  </option>
                )}
              </FormattedMessage>
              {data?.conference.submissionTypes.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name}
                </option>
              ))}
            </Select>
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
              {data.submissions.map((submission) => (
                <VotingCard key={submission.id} submission={submission} />
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
