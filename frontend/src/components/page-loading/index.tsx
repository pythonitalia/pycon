/** @jsx jsx */
import { Box, Heading } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { MetaTags } from "../meta-tags";

export const PageLoading: React.SFC<{ titleId: string }> = ({ titleId }) => (
  <Box sx={{ mx: "auto", py: 5, px: 3, maxWidth: "container" }}>
    <FormattedMessage id={titleId}>
      {(text) => <MetaTags title={text} />}
    </FormattedMessage>

    <Heading sx={{ fontSize: 4 }}>Loading ⌛</Heading>
  </Box>
);
