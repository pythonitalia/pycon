/** @jsx jsx */
import { Box, Grid, Text } from "@theme-ui/components";
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
  topicRank: boolean;
};

export const RankSubmissionRow: React.SFC<Props> = ({
  rankSubmission: { absoluteRank, topicRank, submission },
  backgroundColor,
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
          cursor: "pointer",
          gridTemplateColumns: [`40px 1fr 150px 200px`],
          "svg + svg": {
            marginLeft: [0, 1],
            marginTop: [1, 0],
          },
        }}
      >
        <Box>
          <Text
            variant="label"
            sx={{
              fontWeight: "bold",
              py: 3,
              visibility: ["hidden", "visible"],
            }}
          >
            {topicRank ? topicRank : absoluteRank}
          </Text>
        </Box>
        <Box>
          <Text
            sx={{
              py: 3,
              fontWeight: "bold",
            }}
          >
            <Link
              variant="heading"
              href={`/:language/submission/${submission.id}`}
            >
              {submission.title}
            </Link>
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
              color: "violet",
              textTransform: "uppercase",
            }}
          >
            {submission.speaker?.fullName}
          </Text>
        </Box>
      </Grid>
    </Box>
  </Box>
);
