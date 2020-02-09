/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Grid, Heading, Select, Text } from "@theme-ui/components";
import React from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { useConference } from "../../context/conference";
import {
  RankingSubmissionQuery,
  RankingSubmissionQueryVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { MetaTags } from "../meta-tags";
import { SubmissionAccordion } from "../voting-page/submission-accordion";
import RANKING_SUBMISSION from "./ranking-submissions.graphql";

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

export const RankingPage: React.SFC<RouteComponentProps> = ({ location }) => {
  const { code: conferenceCode } = useConference();
  const { loading, error, data } = useQuery<
    RankingSubmissionQuery,
    RankingSubmissionQueryVariables
  >(RANKING_SUBMISSION, {
    variables: {
      conference: conferenceCode,
    },
  });

  const [filters, { select }] = useFormState();

  return (
    <Box>
      <FormattedMessage id="ranking.seoTitle">
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
                  {text => <option value="">{text}</option>}
                </FormattedMessage>
                {data?.conference.topics.map(topic => (
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
      {data?.conference.ranking && (
        <Box
          as="ul"
          sx={{
            listStyle: "none",
          }}
        >
          {data?.conference.ranking
            .filter(submission => {
              if (
                filters.values.topic &&
                submission.submission.topic?.id !== filters.values.topic
              ) {
                return false;
              }
              return true;
            })
            .map((rankSubmission, index) => (
              <SubmissionAccordion
                showVoting={false}
                renderTitle={title => (
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
