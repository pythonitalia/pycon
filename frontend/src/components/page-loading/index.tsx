/** @jsx jsx */

import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

import { MetaTags } from "../meta-tags";

export const PageLoading: React.SFC<{ titleId: string }> = ({ titleId }) => (
  <Box sx={{ mx: "auto", px: 3, maxWidth: "container" }}>
    <FormattedMessage id={titleId}>
      {(text) => <MetaTags title={text} />}
    </FormattedMessage>

    <Heading sx={{ fontSize: 4 }}>Loading ⌛</Heading>
  </Box>
);
