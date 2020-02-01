/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Grid, Heading, Text } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
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
  console.log(data);
  console.log(error);
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
          {data?.conference.ranking.map((submission, index) => (
            <Text
              sx={{
                py: 3,
              }}
            >
              {submission.submission.title}
            </Text>
          ))}
        </Box>
      )}
    </Box>
  );
};
