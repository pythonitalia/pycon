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
import { SubmissionAccordion } from "~/components/submission-accordion";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useRankingSubmissionQuery } from "~/types";
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

export const RankingPage: React.FC = () => {
  const conferenceCode = process.env.conferenceCode;
  const { loading, data } = useRankingSubmissionQuery({
    variables: {
      conference: conferenceCode,
    },
  });

  const [filters, { select }] = useFormState();
  const filterVisibleSubmissions = (submission) => {
    if (
      filters.values.topic &&
      submission.submission.topic?.id !== filters.values.topic
    ) {
      return false;
    }
    return true;
  };

  if (!loading && !data?.conference?.ranking) {
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
                <FormattedMessage id="ranking.introduction" />
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
                <FormattedMessage id="voting.allTopics">
                  {(text) => <option value="">{text}</option>}
                </FormattedMessage>
                {data?.conference?.topics.map((topic) => (
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
          }}
        >
          {data?.conference?.ranking?.rankedSubmissions
            .filter(filterVisibleSubmissions)
            .map((rankSubmission, index) => (
              <SubmissionAccordion
                renderTitle={(title) => (
                  <React.Fragment>
                    <Text sx={{ fontWeight: "bold" }} as="span">
                      {filters.values.topic
                        ? rankSubmission.topicRank
                        : rankSubmission.absoluteRank}
                      .
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

export default RankingPage;
