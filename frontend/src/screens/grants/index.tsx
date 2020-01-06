/** @jsx jsx */
import { RouteComponentProps } from "@reach/router";
import { Box } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

import { GrantForm } from "../../components/grant-form";
import { Introduction } from "./introduction";

export const GrantScreen: React.SFC<RouteComponentProps> = () => (
  <React.Fragment>
    <Introduction />

    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 3,
        my: 5,
      }}
    >
      <GrantForm />
    </Box>
  </React.Fragment>
);
