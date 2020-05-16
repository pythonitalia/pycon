/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { GrantForm } from "~/components/grant-form";
import { Introduction } from "~/components/grants-introduction";
import { MetaTags } from "~/components/meta-tags";

export default () => {
  const code = process.env.conferenceCode;

  return (
    <React.Fragment>
      <FormattedMessage id="grants.pageTitle">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Introduction />

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
          my: 5,
        }}
      >
        <GrantForm conference={code} />
      </Box>
    </React.Fragment>
  );
};
