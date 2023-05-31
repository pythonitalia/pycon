import {
  MultiplePartsCardCollection,
  Heading,
  Section,
  Text,
  Page,
  Link,
  BasicButton,
  Spacer,
  CardPart,
  MultiplePartsCard,
  Button,
  HorizontalStack,
  FilterBar,
} from "@python-italia/pycon-styleguide";
import React, { useEffect, useState } from "react";
import { FormattedMessage } from "react-intl";

import { GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { MetaTags } from "~/components/meta-tags";
import { VotingCard } from "~/components/voting-card";
import { formatDeadlineDateTime } from "~/helpers/deadlines";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import {
  queryVotingMetadata,
  useVotingMetadataQuery,
  useVotingSubmissionsQuery,
} from "~/types";

type Filters = {
  language?: string;
  voted?: string;
  tags?: string[];
  type?: string;
  audienceLevel?: string;
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
  const [currentFilters, setCurrentFilters] = useState<
    Record<string, string[]>
  >({
    tags: [],
  });
  const [currentPage, setCurrentPage] = useState(1);

  const onUpdateFilters = (nextStateValues) => {
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

    setCurrentFilters(nextStateValues);
  };

  useEffect(() => {
    if (!router.isReady) {
      return;
    }

    setCurrentFilters({
      languages: getAsArray(router.query.language) ?? [],
      voted: router.query.voted ? [router.query.voted.toString()] : [],
      tags: getAsArray(router.query.tags),
      types: getAsArray(router.query.type) ?? [],
      audienceLevels: getAsArray(router.query.audienceLevel) ?? [],
    });

    setCurrentPage(parseInt(router.query.page as string) || 1);
  }, [router.isReady]);

  const { data: votingMetadata } = useVotingMetadataQuery({
    variables: {
      conference: process.env.conferenceCode,
    },
  });

  const { loading, error, data } = useVotingSubmissionsQuery({
    variables: {
      conference: process.env.conferenceCode,
      page: currentPage,
      language,
      languages: currentFilters.languages,
      voted: toBoolean(currentFilters.voted?.[0]),
      tags: currentFilters.tags,
      types: currentFilters.types,
      audienceLevels: currentFilters.audienceLevels,
    },
    skip: !router.isReady || isNaN(currentPage),
    errorPolicy: "all",
  });

  const navigateToPage = (page: number) => {
    setCurrentPage(page);
  };

  const cannotVoteErrors =
    error &&
    error.graphQLErrors.findIndex(
      (e) => e.message === "You need to have a ticket to see submissions",
    ) !== -1;

  const isVotingClosed =
    votingMetadata && !votingMetadata?.conference?.isVotingOpen;
  const userCannotVote =
    loading || (cannotVoteErrors ?? false) || (!!error ?? false);
  const votingDeadline = votingMetadata?.conference?.isVotingOpen
    ? votingMetadata?.conference.votingDeadline?.end
    : undefined;

  const availableFilters = [
    {
      id: "languages",
      label: <FormattedMessage id="scheduleView.filter.byLanguage" />,
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        {
          label: <FormattedMessage id="global.english" />,
          value: "en",
        },
        {
          label: <FormattedMessage id="global.italian" />,
          value: "it",
        },
      ],
    },
    {
      id: "voted",
      label: "By Voted",
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        {
          label: <FormattedMessage id="voting.notVoted" />,
          value: "false",
        },
        {
          label: <FormattedMessage id="voting.votedOnly" />,
          value: "true",
        },
      ],
    },
    {
      id: "types",
      label: <FormattedMessage id="scheduleView.filter.byType" />,
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        ...votingMetadata?.conference.submissionTypes.map((type) => ({
          label: type.name,
          value: type.id,
        })),
      ],
    },
    {
      id: "audienceLevels",
      label: <FormattedMessage id="scheduleView.filter.byAudience" />,
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        ...votingMetadata?.conference.audienceLevels.map((a) => ({
          label: a.name,
          value: a.id,
        })),
      ],
    },
    {
      id: "tags",
      label: <FormattedMessage id="voting.filter.byTag" />,
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        ...votingMetadata?.votingTags.map((tag) => ({
          label: tag.name,
          value: tag.id,
        })),
      ],
    },
  ];

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
        {votingDeadline && router.isReady && (
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
            <Heading>
              <FormattedMessage id="voting.closed.heading" />
            </Heading>
            <Spacer size="small" />
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
                <CardPart contentAlign="left" overflow={true}>
                  <HorizontalStack
                    justifyContent="spaceBetween"
                    alignItems="center"
                  >
                    <Heading size={2}>
                      <FormattedMessage id="voting.proposals" />
                    </Heading>
                    <FilterBar
                      placement="left"
                      onApply={onUpdateFilters}
                      appliedFilters={currentFilters}
                      filters={availableFilters}
                    />
                  </HorizontalStack>
                </CardPart>
              </MultiplePartsCard>
              {data.submissions.items.map((submission) => (
                <VotingCard key={submission.id} submission={submission} />
              ))}
            </MultiplePartsCardCollection>
          </>
        )}
        <Spacer size="xl" />

        {data?.submissions?.pageInfo.totalPages && (
          <Text as="p" size="label1" align="center">
            <FormattedMessage
              id="voting.pagination"
              values={{
                currentPage: currentPage,
                totalPages: data?.submissions?.pageInfo.totalPages,
                totalItems: data?.submissions?.pageInfo.totalItems,
              }}
            />
          </Text>
        )}
        <Spacer size="small" />

        <HorizontalStack
          gap="small"
          alignItems="center"
          justifyContent="center"
        >
          {!isVotingClosed && data?.submissions && (
            <>
              {Array(data.submissions.pageInfo.totalPages)
                .fill(null)
                .map((_, i) => (
                  <Button
                    key={i}
                    background={currentPage === i + 1 ? "green" : undefined}
                    onClick={(_) => {
                      navigateToPage(i + 1);
                    }}
                    size="small"
                    role="secondary"
                  >
                    {i + 1}
                  </Button>
                ))}
            </>
          )}
        </HorizontalStack>
      </Section>
    </Page>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryVotingMetadata(client, {
      conference: process.env.conferenceCode,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default VotingPage;
