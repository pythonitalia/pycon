/** @jsx jsx */

import { Box } from "@theme-ui/components";
import { Link } from "gatsby";
import { jsx } from "theme-ui";

import { BuyTicketsCTA } from "./buy-tickets-cta";
import { Landscape } from "./landscape";

export const HomepageHero: React.SFC = () => (
  <Box
    sx={{
      position: "relative",
      mt: [-100, -180],
    }}
  >
    <Box
      sx={{
        display: "inline-block",
        paddingBottom: ["70vh", "53%"],
      }}
    />

    <Landscape
      sx={{
        position: "absolute",
        left: 0,
        top: 0,
        height: "100%",
        width: "100%",
      }}
    />

    <Box
      sx={{
        position: "absolute",
        bottom: [20, 30],
        left: [0],

        width: "100%",
      }}
    >
      <Box
        sx={{
          maxWidth: "largeContainer",
          width: "100%",
          mx: "auto",
        }}
      >
        <Link
          to="/tickets"
          sx={{
            px: 2,
          }}
        >
          <BuyTicketsCTA
            sx={{
              width: ["20vw", "10vw"],
              height: ["20vw", "10vw"],
            }}
          />
        </Link>
      </Box>
    </Box>
  </Box>
);
