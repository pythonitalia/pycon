/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, Grid, Heading, jsx, Select, Text } from "theme-ui";

import { GetStaticProps } from "next";

import { getApolloClient, addApolloState } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { MetaTags } from "~/components/meta-tags";
import { PageLoading } from "~/components/page-loading";
import { SubmissionAccordion } from "~/components/submission-accordion";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  useRankingQuery,
  useTopicsQuery,
  queryTopics,
  queryRanking,
  RankStat,
} from "~/types";

import ErrorPage from "../_error";

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

type Filters = {
  topic: string;
};
export const RankingPage = () => {
  const conferenceCode = process.env.conferenceCode;

  const {
    data: {
      conference: { topics },
    },
  } = useTopicsQuery({
    variables: {
      code: conferenceCode,
    },
  });
  const [filters, { select }] = useFormState<Filters>({ topic: topics[0].id });

  const { loading, data } = useRankingQuery({
    variables: {
      conference: conferenceCode,
      topic: filters.values.topic,
    },
  });

  const filterVisibleSubmissions = (submission) => {
    if (
      filters.values.topic &&
      submission.submission.topic?.id !== filters.values.topic
    ) {
      return false;
    }
    return true;
  };

  const getRankingStat = (type: string, name: string): RankStat => {
    const stat = data?.conference?.ranking?.stats.filter(
      (stat) =>
        stat.type.toLowerCase() === type &&
        ((name && stat.name.toLowerCase() == name) || !name),
    );
    return stat && stat[0];
  };

  const getRankingStats = (type: string): RankStat[] => {
    return data?.conference?.ranking?.stats.filter(
      (stat) => stat.type.toLowerCase() === type,
    );
  };

  if (loading) {
    return <PageLoading titleId="global.loading" />;
  }

  if (!data?.conference?.ranking) {
    return <ErrorPage statusCode={404} />;
  }

  return (
    <Box>
      <FormattedMessage id="ranking.seoTitle">
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
                <FormattedMessage id="ranking.heading" />
              </Heading>

              <Text my={4}>
                <FormattedMessage
                  id="ranking.introduction"
                  values={{
                    speakersNumber: getRankingStat("speakers", "speakers")
                      ?.value,
                    proposalNumber: getRankingStat("submissions", "submissions")
                      ?.value,
                    br: <br />,
                  }}
                />
              </Text>
            </Box>
            <Box>
              <Select
                {...select("topic")}
                sx={{
                  background: "orange",
                  borderRadius: 0,
                }}
              >
                {topics.map((topic) => (
                  <option key={topic.id} value={topic.id}>
                    {topic.name}
                  </option>
                ))}
              </Select>
            </Box>
          </Grid>

          {loading && (
            <Alert variant="info">
              <FormattedMessage id="voting.loading" />
            </Alert>
          )}
        </Box>
      </Box>
      {data?.conference?.ranking && (
        <Box
          as="ul"
          sx={{
            listStyle: "none",
            mb: 4,
          }}
        >
          {data?.conference?.ranking?.rankedSubmissions
            .filter(filterVisibleSubmissions)
            .map((rankSubmission, index) => (
              <SubmissionAccordion
                renderTitle={(title) => (
                  <React.Fragment>
                    <Text sx={{ fontWeight: "bold" }} as="span">
                      {rankSubmission.rank}
                    </Text>{" "}
                    {title}
                  </React.Fragment>
                )}
                showVoting={false}
                backgroundColor={COLORS[index % COLORS.length].background}
                headingColor={COLORS[index % COLORS.length].heading}
                key={rankSubmission.submission.id}
                submission={rankSubmission.submission}
              />
            ))}
        </Box>
      )}

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
          mb: 4,
        }}
      >
        <Heading mb={4}>
          <FormattedMessage id="ranking.stats.heading" />
        </Heading>
        <Grid
          gap={4}
          sx={{
            gridTemplateColumns: [null, "1fr 1fr"],
          }}
        >
          <Box>
            <Text>
              <FormattedMessage
                id="ranking.stats.submissions"
                values={{
                  value: getRankingStat("submissions", "submissions")?.value,
                }}
              />
            </Text>
            <Text>
              <FormattedMessage
                id="ranking.stats.speakers"
                values={{
                  value: getRankingStat("speakers", "speakers")?.value,
                }}
              />
            </Text>
            <Text>
              <FormattedMessage
                id="ranking.stats.gender.women"
                values={{
                  value: getRankingStat("gender", "female")?.value,
                }}
              />
            </Text>
            <Text>
              <FormattedMessage
                id="ranking.stats.gender.women"
                values={{
                  value: getRankingStat("gender", "male")?.value,
                }}
              />
            </Text>

            <Text>
              <FormattedMessage
                id="ranking.stats.language.italian"
                values={{
                  value: getRankingStat("language", "italian")?.value,
                }}
              />
            </Text>
            <Text>
              <FormattedMessage
                id="ranking.stats.language.english"
                values={{
                  value: getRankingStat("language", "english")?.value,
                }}
              />
            </Text>
          </Box>
          <Box>
            {getRankingStats("submission_type").map((stat) => (
              <Text>
                <FormattedMessage
                  id="ranking.stats.submissionType"
                  values={{
                    value: stat.value,
                    name: stat.name,
                  }}
                />
              </Text>
            ))}
            {getRankingStats("audience_level").map((stat) => (
              <Text>
                <FormattedMessage
                  id="ranking.stats.audienceLevel"
                  values={{
                    value: stat.value,
                    name: stat.name,
                  }}
                />
              </Text>
            ))}
          </Box>
        </Grid>
      </Box>
    </Box>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  const {
    data: {
      conference: { topics },
    },
  } = await queryTopics(client, {
    code: process.env.conferenceCode,
  });

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryRanking(client, {
      conference: process.env.conferenceCode,
      topic: topics[0].id,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default RankingPage;
