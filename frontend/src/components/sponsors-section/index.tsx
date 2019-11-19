/** @jsx jsx */
import css from "@styled-system/css";
import { Box, Heading } from "@theme-ui/components";
import { jsx } from "theme-ui";

import { HomePageQuery } from "../../generated/graphql";
import { SponsorsGrid } from "./sponsors-grid";

type Props = {
  sponsorsByLevel: HomePageQuery["backend"]["conference"]["sponsorsByLevel"];
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
              p: 2,
              left: -20,
            }}
            css={css`
              @media (min-width: 1310px) {
                position: relative;
                display: inline-block;
                padding: 0;
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
