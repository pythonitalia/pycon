/** @jsxRuntime classic */

/** @jsx jsx */
import React, { Fragment } from "react";
import { Box, Flex, Heading, jsx, Text } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { SocialSnakes } from "~/components/illustrations/social-snakes";
import { CardType, getSize, getTitleFontSize } from "~/helpers/social-card";
import { useCurrentLanguage } from "~/locale/context";
import { queryBlogSocialCard, useBlogSocialCardQuery } from "~/types";

export const SocialCard = () => {
  const router = useRouter();
  const cardType = (router.query["card-type"] as CardType) || "social";
  const slug = router.query.slug as string;
  const language = useCurrentLanguage();

  const { data, loading } = useBlogSocialCardQuery({
    variables: {
      slug,
      language,
    },
  });

  if (loading) {
    return null;
  }

  const post = data.blogPost;

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
            {post.author.fullName}
          </Text>

          <Heading
            variant="caps"
            sx={{
              fontSize: getTitleFontSize(cardType),
              fontWeight: "bold",
            }}
          >
            {post.title}
          </Heading>
        </Box>

        <SocialSnakes
          sx={{ position: "absolute", bottom: -14, right: 100, width: 170 }}
        />
      </Flex>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ params, locale }) => {
  const slug = params.slug as string;
  const client = getApolloClient();

  await queryBlogSocialCard(client, {
    slug,
    language: locale,
  });

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () => ({
  paths: [],
  fallback: "blocking",
});

export default SocialCard;
