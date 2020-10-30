/** @jsx jsx */
import { Box, jsx } from "theme-ui";

import { Link } from "../link";
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
        bottom: -50,
        left: 0,
        zIndex: 1,
        width: "100%",
      }}
    >
      <Box
        sx={{
          px: 3,
          maxWidth: "container",
          width: "100%",
          mx: "auto",
        }}
      >
        <Link path="/[lang]/tickets">
          <BuyTicketsCTA
            sx={{
              width: 122,
              height: 122,
            }}
          />
        </Link>
      </Box>
    </Box>
  </Box>
);
