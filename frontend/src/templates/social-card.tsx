/** @jsx jsx */
import { Box, Flex, Heading } from "@theme-ui/components";
import { graphql } from "gatsby";
import { Fragment } from "react";
import { jsx } from "theme-ui";

import { MainIllustration } from "../components/illustrations/main";
import { LogoOrange } from "../components/logo/orange";
import { SocialCardQuery } from "../generated/graphql";

const getDays = ({ start, end }: { start: string; end: string }) => {
  // assuming the same month
  const startDate = new Date(start);
  const endDate = new Date(end);

  return `${startDate.getDate()} - ${endDate.getDate()}`;
};

const getMonth = ({ end }: { end: string }) => {
  const endDate = new Date(end);

  const formatter = new Intl.DateTimeFormat("default", {
    month: "long",
  });

  return formatter.format(endDate);
};

const getYear = ({ end }: { end: string }) => {
  const endDate = new Date(end);

  return endDate.getFullYear();
};

export default ({ data }: { data: SocialCardQuery }) => (
  <Fragment>
    <Flex
      sx={{
        width: 1200,
        height: 630,
        overflow: "hidden",
      }}
    >
      <MainIllustration />

      <Flex sx={{ flexDirection: "column", ml: -14 }}>
        <LogoOrange />

        <Flex
          sx={{
            flex: 1,
            flexDirection: "column",
            border: "14px solid black",
            borderTop: "none",
            backgroundColor: "#34B4A1",
            p: 5,
          }}
        >
          <Heading
            sx={{
              textTransform: "uppercase",
              fontSize: 6,
              mb: 2,
              fontWeight: "bold",
            }}
          >
            Florence
          </Heading>

          <Heading
            sx={{
              textTransform: "uppercase",
              fontSize: 6,
              mb: 2,
              fontWeight: "bold",
            }}
          >
            {getDays(data.backend.conference)}
          </Heading>

          <Heading
            sx={{
              textTransform: "uppercase",
              fontSize: 6,
              mb: 2,
              fontWeight: "bold",
            }}
          >
            {getMonth(data.backend.conference)}{" "}
            {getYear(data.backend.conference)}
          </Heading>
          <Heading
            sx={{
              textTransform: "uppercase",
              fontSize: 6,
              fontWeight: "bold",
              color: "white",
              mt: "auto",
            }}
          >
            {data.backend.conference.name}
          </Heading>
        </Flex>
      </Flex>
    </Flex>
  </Fragment>
);

export const query = graphql`
  query SocialCard {
    backend {
      conference {
        start
        end
        name
      }
    }
  }
`;
