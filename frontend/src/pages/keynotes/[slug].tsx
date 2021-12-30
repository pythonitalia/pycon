/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment, useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Grid, Flex, Heading, jsx, Text } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import Image from "next/image";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Article } from "~/components/article";
import { BlogPostIllustration } from "~/components/illustrations/blog-post";
import { KeynoteSlide } from "~/components/keynoters-section/keynote-slide";
import { Link } from "~/components/link";
import { Marquee } from "~/components/marquee";
import { MetaTags } from "~/components/meta-tags";
import { compile } from "~/helpers/markdown";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryAllKeynotes, queryKeynote, useKeynoteQuery } from "~/types";

type KeynoteInfoLineProps = {
  property: string;
  value: string;
  to?: string;
};

const KeynoteInfoLine = ({ property, value, to }: KeynoteInfoLineProps) => (
  <Grid
    gap={0}
    sx={{
      gridTemplateColumns: [null, "0.3fr 1fr"],
      borderBottom: "2px solid",
      borderColor: "violet",
      mb: 3,
      pb: [3, 2],
    }}
  >
    <Text
      sx={{
        textTransform: "uppercase",
        fontWeight: "bold",
        color: "violet",
        userSelect: "none",
      }}
    >{`${property}:`}</Text>
    <Text>
      {to ? (
        <Link
          sx={{
            color: "black",
          }}
          external
          path={to}
          target="_blank"
          rel="noopener noreferrer"
        >
          {value}
        </Link>
      ) : (
        value
      )}
    </Text>
  </Grid>
);

const KeynotePage = () => {
  const {
    query: { slug },
    push,
  } = useRouter();
  const {
    data: {
      conference: {
        keynote: { keynoteTitle, keynoteDescription, speakers },
      },
    },
  } = useKeynoteQuery({
    variables: {
      conference: process.env.conferenceCode,
      slug,
    },
  });
  const goBack = useCallback(() => {
    push("/keynotes");
  }, []);
  const firstSpeaker = speakers[0];
  return (
    <Fragment>
      <MetaTags title={keynoteTitle} />
      <Box
        sx={{
          borderTop: "primary",
        }}
      />

      <Grid
        gap={[0, null, 5]}
        sx={{
          mx: "auto",
          px: 3,
          py: 5,
          maxWidth: "container",
          gridTemplateColumns: [null, null, "1.5fr 1fr"],
        }}
      >
        <Box>
          <Article title={keynoteTitle}>
            <Box>{compile(keynoteDescription).tree}</Box>
          </Article>
        </Box>
        <Box sx={{ mb: 5 }}>
          <Flex
            sx={{
              position: "relative",
              justifyContent: "flex-end",
              alignItems: "flex-start",
            }}
          >
            <BlogPostIllustration
              sx={{
                width: "80%",
              }}
            />

            <Box
              sx={{
                border: "primary",
                p: 4,
                backgroundColor: "cinderella",
                width: "80%",
                position: "absolute",
                left: 0,
                top: "90%",
              }}
            >
              <Text sx={{ fontWeight: "bold" }}>
                <FormattedMessage id="keynote.speakers" />
              </Text>

              <Text>{speakers.map((speaker) => speaker.name).join(" & ")}</Text>
            </Box>
          </Flex>
        </Box>
      </Grid>

      <Box
        sx={{
          borderTop: "primary",
          pb: 4,
        }}
      />

      {speakers.map((speaker) => (
        <Grid
          gap={[3, 5]}
          sx={{
            mx: "auto",
            px: 3,
            py: 4,
            maxWidth: "container",
            gridTemplateColumns: [null, null, "0.5fr 1fr"],
          }}
        >
          <KeynoteSlide
            keynoteTitle=""
            standalone
            slug={null}
            speakers={[speaker]}
          />

          <Box>
            {speaker.website && (
              <KeynoteInfoLine
                property="Website"
                value={speaker.website}
                to={speaker.website}
              />
            )}
            {speaker.twitterHandle && (
              <KeynoteInfoLine
                property="Twitter"
                value={`@${speaker.twitterHandle}`}
                to={`https://twitter.com/${speaker.twitterHandle}`}
              />
            )}
            {speaker.instagramHandle && (
              <KeynoteInfoLine
                property="Instagram"
                value={`@${speaker.instagramHandle}`}
                to={`https://instagram.com/${speaker.instagramHandle}`}
              />
            )}
            {speaker.pronouns && (
              <KeynoteInfoLine property="Pronouns" value={speaker.pronouns} />
            )}
            <Text>{speaker.bio}</Text>
          </Box>
        </Grid>
      ))}

      <Box
        sx={{
          pt: 4,
        }}
      />

      <Box
        sx={{
          color: "black",
          cursor: "pointer",
        }}
        onClick={goBack}
      >
        <Marquee separator=">" message="Back to Keynotes" />
      </Box>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale, params }) => {
  const slug = params.slug as string;
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryKeynote(client, {
      conference: process.env.conferenceCode,
      slug,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () => {
  const client = getApolloClient();
  const {
    data: {
      conference: { keynotes },
    },
  } = await queryAllKeynotes(client, {
    conference: process.env.conferenceCode,
  });
  const paths = [
    ...keynotes.map((keynote) => ({
      params: {
        slug: keynote.slug,
      },
      locale: "en",
    })),
    ...keynotes.map((keynote) => ({
      params: {
        slug: keynote.slug,
      },
      locale: "it",
    })),
  ];

  return {
    paths,
    fallback: "blocking",
  };
};

export default KeynotePage;
