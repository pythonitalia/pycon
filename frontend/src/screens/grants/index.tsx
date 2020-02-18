/** @jsx jsx */
import { RouteComponentProps } from "@reach/router";
import { Box } from "@theme-ui/components";
import React from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { GrantForm } from "../../components/grant-form";
import { MetaTags } from "../../components/meta-tags";
import { useConference } from "../../context/conference";
import { Introduction } from "./introduction";

export const GrantScreen: React.SFC<RouteComponentProps> = () => {
  const { code } = useConference();

  return (
    <React.Fragment>
      <FormattedMessage id="grants.pageTitle">
        {text => <MetaTags title={text} />}
      </FormattedMessage>
      <Introduction />

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
