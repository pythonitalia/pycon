/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Grid, Heading, Select, Text } from "@theme-ui/components";
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
import RANKING_SUBMISSION from "./ranking-submissions.graphql";
import { RankSubmissionRow } from "./submission-row";

const COLORS = ["blue", "lightBlue"];

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

  console.log(data);
  console.log(error);

  const [filters, { select }] = useFormState();

  // @ts-ignore
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
        </Box>
      </Box>
      {loading && (
        <Alert variant="info">
          <FormattedMessage id="voting.loading" />
        </Alert>
      )}
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
              <RankSubmissionRow
                key={rankSubmission.submission.id}
                rankSubmission={rankSubmission}
                backgroundColor={COLORS[index % COLORS.length]}
                topicRank={!!filters.values.topic}
              />
            ))}
        </Box>
      )}
    </Box>
  );
};
