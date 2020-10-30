/** @jsx jsx */

import { Box, Heading, jsx } from "theme-ui";

import { SponsorsGrid } from "./sponsors-grid";
import { Sponsor } from "./types";

type Props = {
  sponsorsByLevel: {
    level: string;
    sponsors: Sponsor[];
    highlightColor?: string | null;
  }[];
};

export const SponsorsSection: React.SFC<Props> = ({
  sponsorsByLevel,
  ...props
}) => (
  <Box {...props}>
    {sponsorsByLevel.map(({ level, sponsors, highlightColor }) => (
      <Box key={level}>
        <Heading
          sx={{
            maxWidth: "container",
            mx: "auto",
            my: 3,
          }}
        >
          <Box
            as="span"
            sx={{
              transform: "rotate(90deg)",
              transformOrigin: "0 0",
              top: 5,
              py: 2,
              px: 3,
              left: -20,
            }}
            css={`
              @media (min-width: 1310px) {
                position: static;
                display: inline-block;
                padding: 0;
                transform: none;
              }
            `}
          >
            {level}
          </Box>
        </Heading>

        <SponsorsGrid color={highlightColor} sponsors={sponsors} />
      </Box>
    ))}
  </Box>
);
