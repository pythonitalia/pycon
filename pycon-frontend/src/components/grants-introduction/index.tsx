/** @jsxRuntime classic */
/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, Grid, jsx, Text } from "theme-ui";

import { CFPIllustration } from "~/components/illustrations/cfp";
import { Link } from "~/components/link";

export const Introduction: React.SFC = () => (
  <Box
    sx={{
      borderTop: "primary",
      borderBottom: "primary",
    }}
  >
    <Grid
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 3,
        my: 5,
        gridTemplateColumns: [null, null, "9fr 3fr 5fr"],
      }}
    >
      <Box>
        <Text as="h1">
          <FormattedMessage id="grants.introductionHeading" />
        </Text>
        <Text
          as="p"
          sx={{
            color: "orange",
            mt: 4,
            fontSize: 2,
          }}
        >
          <FormattedMessage id="grants.introductionSubtitle" />
        </Text>
        <Text
          sx={{
            mt: 4,
            fontSize: 2,
          }}
          as="p"
        >
          <FormattedMessage id="grants.introductionCopy" />
        </Text>

        <Link path="/[lang]/grants-info" variant="button" sx={{ mt: 4 }}>
          <FormattedMessage id="grants.learnMore" />
        </Link>
      </Box>
      <Box
        sx={{
          gridColumnStart: [0, 0, 3],
        }}
      >
        <Box
          sx={{
            display: ["none", null, "block"],
            border: "primary",
            gridColumnStart: [0, 0, 3],
            backgroundColor: "#C4C4C4",
            position: "relative",
          }}
        >
          <Box sx={{ display: "inline-block", pt: "100%", width: "100%" }} />
          <CFPIllustration
            sx={{
              position: "absolute",
              top: 0,
              left: "-4px",
              width: "100%",
              height: "100%",
            }}
          />
        </Box>
      </Box>
    </Grid>
  </Box>
);
