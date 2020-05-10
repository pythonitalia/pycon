/** @jsx jsx */
import { Box, Flex, Heading } from "@theme-ui/components";
import { Fragment } from "react";
import { jsx } from "theme-ui";

import { LogoOrange } from "~/components/logo/orange";
import { getSize } from "~/helpers/social-card";
import { useSocialCardQuery } from "~/types";

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

export default () => {
  const { data } = useSocialCardQuery({
    variables: {
      code: process.env.conferenceCode,
    },
  });

  const size = getSize("social-twitter");
  const padding = 14;

  if (!data) {
    return null;
  }

  return (
    <Fragment>
      <Box
        sx={{
          ...size,
          overflow: "hidden",
          background: "black",
          p: padding,
        }}
      >
        <Flex>
          <img
            src="/images/main-illustration.png"
            sx={{
              height: size.height - padding * 2,
              width: size.height - padding * 2,
            }}
          />

          <Flex
            sx={{
              flexDirection: "column",
              ml: -14,
              width: size.width - size.height,
            }}
          >
            <LogoOrange
              sx={{
                width: size.width - size.height,
              }}
            />

            <Flex
              sx={{
                flexDirection: "column",
                border: "14px solid black",
                borderTop: "none",
                backgroundColor: "#34B4A1",
                flex: 1,
                width: size.width - size.height + 14 - padding,
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
                {getDays(data.conference)}
              </Heading>

              <Heading
                sx={{
                  textTransform: "uppercase",
                  fontSize: 6,
                  mb: 2,
                  fontWeight: "bold",
                }}
              >
                {getMonth(data.conference)} {getYear(data.conference)}
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
                {data.conference.name}
              </Heading>
            </Flex>
          </Flex>
        </Flex>
      </Box>
    </Fragment>
  );
};
