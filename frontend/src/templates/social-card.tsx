/** @jsx jsx */
import { Box, Flex, Heading } from "@theme-ui/components";
import { graphql } from "gatsby";
import { Fragment } from "react";
import { jsx } from "theme-ui";

import { LogoOrange } from "../components/logo/orange";
import { SocialCardQuery } from "../generated/graphql";
import { CardType, getSize } from "../helpers/social-card";

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

type Props = {
  data: SocialCardQuery;
  pageContext: {
    cardType: CardType;
  };
};

export default ({ data, pageContext }: Props) => {
  const size = getSize(pageContext.cardType);
  const padding = pageContext.cardType === "social-twitter" ? 14 : 0;

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
            src={data.file!.childImageSharp!.fixed!.src!}
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
                width: size.width - size.height + 14,
              }}
            />

            <Flex
              sx={{
                flexDirection: "column",
                border: "14px solid black",
                borderTop: "none",
                borderRight:
                  pageContext.cardType === "social-twitter" ? "none" : "",
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
      </Box>
    </Fragment>
  );
};

export const query = graphql`
  query SocialCard {
    backend {
      conference {
        start
        end
        name
      }
    }

    file(relativePath: { eq: "images/main-illustration.png" }) {
      childImageSharp {
        fixed(width: 1260, height: 1260) {
          src
        }
      }
    }
  }
`;
