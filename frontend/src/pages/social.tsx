/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment } from "react";
import { Box, Flex, Heading, jsx } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Logo } from "~/components/logo";
import { CardType, getSize } from "~/helpers/social-card";
import { useCurrentLanguage } from "~/locale/context";
import { Language } from "~/locale/languages";
import { querySocialCard, useSocialCardQuery } from "~/types";

const getDays = ({ start, end }: { start: string; end: string }) => {
  // assuming the same month
  const startDate = new Date(start);
  const endDate = new Date(end);

  return `${startDate.getUTCDate()} - ${endDate.getUTCDate()}`;
};

const getMonth = ({ end }: { end: string }, language: Language) => {
  const endDate = new Date(end);

  const formatter = new Intl.DateTimeFormat(language, {
    month: "long",
  });

  return formatter.format(endDate);
};

const getYear = ({ end }: { end: string }) => {
  const endDate = new Date(end);

  return endDate.getFullYear();
};

export const SocialPage = () => {
  const router = useRouter();
  const language = useCurrentLanguage();
  const { data } = useSocialCardQuery({
    variables: {
      code: process.env.conferenceCode,
    },
  });
  const cardType = (router.query["card-type"] as CardType) || "social";

  const size = getSize(cardType);
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
        id="social-card"
      >
        <Flex>
          <img
            src="/images/main-illustration.png"
            alt=""
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
            <Logo
              sx={{
                width: `calc(${size.width - size.height}px - 14px)`,
                ml: "7px",
                mt: "7px",
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
                {getMonth(data.conference, language)} {getYear(data.conference)}
              </Heading>
              <Heading
                sx={{
                  textTransform: "uppercase",
                  fontSize: 5,
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

export const getStaticProps: GetStaticProps = async () => {
  const client = getApolloClient();

  await querySocialCard(client, {
    code: process.env.conferenceCode,
  });

  return addApolloState(client, {
    props: {},
  });
};

export default SocialPage;
