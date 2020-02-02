/** @jsx jsx */
import { Box, Grid, Text } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { Scalars } from "../../generated/graphql-backend";
import { Link } from "../link";

type RankSubmission = {
  absoluteRank: Scalars["Int"];
  topicRank: Scalars["Int"];
  submission: {
    id: Scalars["ID"];
    title: string;
    topic: {
      id: string;
      name: string;
    } | null;
    speaker: {
      fullName: string;
    } | null;
  };
};

type Props = {
  rankSubmission: RankSubmission;
  backgroundColor: string;
  filterByTopic: boolean;
};

export const RankSubmissionRow: React.SFC<Props> = ({
  rankSubmission: { absoluteRank, topicRank, submission },
  backgroundColor,
  filterByTopic,
}) => (
  <Box
    as="li"
    sx={{
      backgroundColor,
      overflow: "hidden",
    }}
  >
    <Box
      sx={{
        borderTop: "primary",
      }}
    >
      <Grid
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
          justifyContent: "space-between",
          alignItems: "center",
          gridTemplateColumns: [`40px 1fr 150px 200px 60px`],
          "svg + svg": {
            marginLeft: [0, 1],
            marginTop: [1, 0],
          },
        }}
      >
        <Box>
          <Text
            sx={{
              fontWeight: "bold",
              py: 3,
              visibility: ["hidden", "visible"],
              textAlign: "right",
            }}
          >
            {filterByTopic ? topicRank : absoluteRank}
          </Text>
        </Box>
        <Box>
          <Text
            sx={{
              fontWeight: "bold",
              py: 3,
              fontWeight: "bold",
            }}
          >
            {submission.title}
          </Text>
        </Box>
        <Box>
          <Text
            sx={{
              py: 3,
              fontWeight: "bold",
            }}
          >
            {submission.topic?.name}
          </Text>
        </Box>
        <Box>
          <Text
            sx={{
              py: 3,
              fontWeight: "bold",
              textTransform: "uppercase",
            }}
          >
            {submission.speaker?.fullName}
          </Text>
        </Box>
        <Box as="footer">
          <Link
            variant="button"
            href={`/:language/submission/${submission.id}`}
          >
            <FormattedMessage id="ranking.details" />
          </Link>
        </Box>
      </Grid>
    </Box>
  </Box>
);
