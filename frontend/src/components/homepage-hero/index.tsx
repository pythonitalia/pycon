/** @jsxRuntime classic */

/** @jsx jsx */
import { Box, jsx } from "theme-ui";

import { Link } from "../link";
import { BuyTicketsCTA } from "./buy-tickets-cta";
import { Landscape } from "./landscape";

type Props = {
  hideBuyTickets?: boolean;
};

export const HomepageHero = ({ hideBuyTickets = false }: Props) => (
  <Box
    sx={{
      position: "relative",
      mt: -130,
    }}
  >
    <Box
      sx={{
        display: "inline-block",
        paddingBottom: ["70vh", "calc(100vh - 125px)"],
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

    {!hideBuyTickets && (
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
          <Link path="/tickets">
            <BuyTicketsCTA
              sx={{
                width: 122,
                height: 122,
              }}
            />
          </Link>
        </Box>
      </Box>
    )}
  </Box>
);
