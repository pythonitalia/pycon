/** @jsx jsx */
import { RouteComponentProps } from "@reach/router";
import { Box, Grid, Heading, Text } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
import { MetaTags } from "../meta-tags";
import { jsx } from "theme-ui";

export const RankingPage: React.SFC<RouteComponentProps> = ({ location }) => {
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
    </Box>
  );
};
