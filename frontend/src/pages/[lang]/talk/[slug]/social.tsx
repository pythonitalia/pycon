/** @jsx jsx */

import { useRouter } from "next/router";
import React, { Fragment } from "react";
import { Box, Flex, Heading, jsx, Text } from "theme-ui";

import { CardType, getSize } from "~/helpers/social-card";
import { useTalkSocialCardQuery } from "~/types";

const Snakes: React.SFC = (props) => (
  <svg fill="none" viewBox="0 0 170 200" {...props}>
    <path
      d="M164.786 191.282c0 .022.023 7.829 0 7.829H140.89v-.308c9.139-9.482 9.139-28.472 0-37.954-9.14-9.493-9.14-28.471 0-37.953 9.139-9.494 9.139-28.472 0-37.968-9.14-9.482-9.14-28.46 0-37.953 9.139-9.494 7.957-28.472-1.18-37.968l.023-.06c14.852 7.737 25.053 23.56 25.053 41.392v140.943z"
      fill="#FCE8DE"
    />
    <path
      d="M140.89 84.928c9.139 9.493 9.139 28.471 0 37.968-9.14 9.482-9.14 28.46 0 37.953 9.139 9.482 9.139 28.472 0 37.954v.308h-23.011c.023 0 0 .13 0-7.83V50.339c0-16.675-8.913-31.59-22.21-39.784a45.373 45.373 0 0122.717-6.625 44.057 44.057 0 0121.347 5.02l-.023.06c9.14 9.493 10.319 28.471 1.18 37.967-9.14 9.496-9.14 28.469 0 37.95z"
      fill="#F17A5D"
    />
    <path
      d="M95.67 10.555a45.373 45.373 0 0122.716-6.625 44.057 44.057 0 0121.347 5.02c14.852 7.736 25.053 23.56 25.053 41.392v140.942c0 .023.022 7.83 0 7.83h-46.907"
      stroke="#000"
      strokeWidth={6}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path
      d="M95.67 10.555c13.293 8.194 22.209 23.11 22.209 39.784v140.943c0 7.959.023 7.829 0 7.829M140.89 198.805c9.139-9.482 9.139-28.471 0-37.953-9.14-9.493-9.14-28.471 0-37.953 9.139-9.494 9.139-28.472 0-37.968-9.14-9.482-9.14-28.46 0-37.954 9.139-9.493 7.957-28.471-1.18-37.967"
      stroke="#000"
      strokeWidth={6}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path
      d="M91.676 62.02v137.445c0 .023-.022.034-.045.034H68.915c8.452-8.924 8.415-26.601-.116-35.457-8.565-8.891-8.565-26.684 0-35.585 8.565-8.891 8.565-26.684 0-35.585-8.565-8.891-8.565-26.684 0-35.586 8.452-8.763 7.495-26.199-.761-35.217 14.06 7.694 23.638 22.872 23.638 39.951z"
      fill="#F17A5D"
    />
    <path
      d="M68.8 92.871c8.565 8.902 8.565 26.695 0 35.586-8.566 8.901-8.566 26.694 0 35.585 8.53 8.856 8.565 26.533.116 35.457H45.982c-.023 0-.046-.011-.046-.034V61.132c0-.012-.01-.034-.033-.034H3.045c-.022 0-.045-.023-.045-.034.023-24.173 19.377-43.82 43.429-44.303 7.818-.162 15.175 1.797 21.61 5.308 8.253 9.018 9.21 26.451.76 35.217-8.565 8.902-8.565 26.695 0 35.585zM38.104 36.916a3.676 3.676 0 00-3.673-3.673 3.676 3.676 0 00-3.673 3.673 3.676 3.676 0 003.673 3.673 3.676 3.676 0 003.673-3.673z"
      fill="#FCE8DE"
    />
    <path
      d="M34.433 40.589a3.673 3.673 0 100-7.346 3.673 3.673 0 000 7.346z"
      fill="#000"
    />
    <path
      d="M68.916 199.499H45.982c-.023 0-.046-.011-.046-.034V61.132c0-.012-.01-.034-.033-.034H3.045c-.022 0-.045-.023-.045-.034.023-24.173 19.377-43.82 43.429-44.303 7.818-.162 15.175 1.797 21.61 5.308 14.057 7.694 23.638 22.872 23.638 39.948v137.446c0 .022-.023.034-.045.034H68.916v.002z"
      stroke="#000"
      strokeWidth={6}
      strokeMiterlimit={1}
    />
    <path
      d="M68.799 199.624c.034-.046.08-.079.116-.128 8.452-8.924 8.415-26.601-.116-35.457-8.565-8.891-8.565-26.683 0-35.585 8.565-8.891 8.565-26.684 0-35.586-8.565-8.89-8.565-26.683 0-35.585 8.452-8.763 7.495-26.199-.761-35.217-.105-.127-.218-.24-.334-.368"
      stroke="#000"
      strokeWidth={6}
      strokeMiterlimit={10}
    />
  </svg>
);

type Props = {};

const getTitleFontSize = (cardType: CardType) => {
  switch (cardType) {
    case "social":
    case "social-twitter":
      return 7;
    case "social-square":
      return 8;
  }
};

export const SocialCard: React.FC<Props> = () => {
  const router = useRouter();
  const cardType = (router.query["card-type"] as CardType) || "social";
  const slug = router.query.slug as string;
  const code = process.env.conferenceCode;

  const { loading, data } = useTalkSocialCardQuery({
    variables: {
      slug,
      code,
    },
  });

  if (loading) {
    return null;
  }

  const talk = data.conference.talk;

  return (
    <Fragment>
      <Flex
        sx={{
          ...getSize(cardType),
          position: "relative",
          overflow: "hidden",
          border: "socialCard",
          background: "orange",
          flexDirection: "column",
          justifyContent: "center",
          px: 5,
        }}
        id="social-card"
      >
        <Box sx={{ position: "relative" }}>
          <Text
            sx={{
              color: "white",
              fontSize: 6,
              position: "absolute",
              bottom: "100%",
              mb: 3,
            }}
          >
            {talk.speakers.map((speaker) => speaker.fullName).join("&")}
          </Text>

          <Heading
            variant="caps"
            sx={{
              fontSize: getTitleFontSize(cardType),
              fontWeight: "bold",
            }}
          >
            {talk.title}
          </Heading>
        </Box>

        <Snakes
          sx={{ position: "absolute", bottom: -14, right: 100, width: 170 }}
        />
      </Flex>
    </Fragment>
  );
};

export default SocialCard;
