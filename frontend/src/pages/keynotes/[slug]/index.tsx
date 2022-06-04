/** @jsxRuntime classic */

/** @jsx jsx */
import React, { Fragment, useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Grid, Flex, jsx, Text } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Article } from "~/components/article";
import { BackToMarquee } from "~/components/back-to-marquee";
import { BlogPostIllustration } from "~/components/illustrations/blog-post";
import { KeynoteSlide } from "~/components/keynoters-section/keynote-slide";
import { Link } from "~/components/link";
import { MetaTags } from "~/components/meta-tags";
import { compile } from "~/helpers/markdown";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { queryAllKeynotes, queryKeynote, useKeynoteQuery } from "~/types";

type KeynoteInfoLineProps = {
  property: string | React.ReactNode;
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
    >
      {property}:
    </Text>
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
  const language = useCurrentLanguage();
  const {
    query: { slug, day },
    push,
  } = useRouter();
  const {
    data: {
      conference: {
        keynote: { title, description, topic, speakers },
      },
    },
  } = useKeynoteQuery({
    variables: {
      conference: process.env.conferenceCode,
      slug: slug as string,
      language,
    },
  });

  const goBack = useCallback(() => {
    if (day) {
      push(`/schedule/${day}`);
    } else {
      push("/keynotes");
    }
  }, [day]);

  const speakersName = speakers.map((speaker) => speaker.name).join(" & ");

  return (
    <Fragment>
      <FormattedMessage
        id="keynote.socialDescription"
        values={{
          speakersName,
        }}
      >
        {(socialDescription) => (
          <MetaTags
            title={title}
            description={socialDescription.join(" ")}
            useDefaultSocialCard={false}
          />
        )}
      </FormattedMessage>
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
          <Article title={title}>
            <Box>{compile(description).tree}</Box>
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

            <Grid
              gap={2}
              sx={{
                border: "primary",
                p: 4,
                backgroundColor: "cinderella",
                width: "80%",
                position: "absolute",
                left: 0,
                top: topic ? "60%" : "70%",
              }}
            >
              <Box>
                <Text sx={{ fontWeight: "bold" }}>
                  <FormattedMessage id="keynote.speakers" />
                </Text>

                <Text>{speakersName}</Text>
              </Box>

              <Box>
                <Text sx={{ fontWeight: "bold" }}>
                  <FormattedMessage id="keynote.language" />
                </Text>

                <Text>
                  <FormattedMessage id="keynote.englishLanguage" />
                </Text>
              </Box>

              {topic && (
                <Box>
                  <Text sx={{ fontWeight: "bold" }}>
                    <FormattedMessage id="keynote.topic" />
                  </Text>

                  <Text>{topic.name}</Text>
                </Box>
              )}
            </Grid>
          </Flex>
          <Link
            path="https://app.sli.do/event/aky15QGFg4bx7o1Lv1VEjw?section=f1d73b4c-9146-49ad-892f-e98c3f24b65e"
            variant="button"
            target="_blank"
            sx={{
              backgroundColor: "yellow",
              width: "fit-content",
              py: 1,
              mt: [0, 2, 6],
              mb: [2, 0],
              position: "relative",
              textTransform: "none",
              "&:hover": {
                backgroundColor: "orange",
              },
            }}
          >
            <FormattedMessage id="streaming.qa" />
          </Link>
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
          <KeynoteSlide title="" standalone slug={null} speakers={[speaker]} />

          <Box>
            {speaker.website && (
              <KeynoteInfoLine
                property={<FormattedMessage id="keynote.website" />}
                value={speaker.website}
                to={speaker.website}
              />
            )}
            {speaker.twitterHandle && (
              <KeynoteInfoLine
                property={<FormattedMessage id="keynote.twitter" />}
                value={`@${speaker.twitterHandle}`}
                to={`https://twitter.com/${speaker.twitterHandle}`}
              />
            )}
            {speaker.instagramHandle && (
              <KeynoteInfoLine
                property={<FormattedMessage id="keynote.instagram" />}
                value={`@${speaker.instagramHandle}`}
                to={`https://instagram.com/${speaker.instagramHandle}`}
              />
            )}
            {speaker.pronouns && (
              <KeynoteInfoLine
                property={<FormattedMessage id="keynote.pronouns" />}
                value={speaker.pronouns}
              />
            )}
            {speaker.bio && <Text>{compile(speaker.bio).tree}</Text>}
          </Box>
        </Grid>
      ))}
      <BackToMarquee backTo={day ? "schedule" : "keynotes"} goBack={goBack} />
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
      language: locale,
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
      conference: { keynotes: italianKeynotes },
    },
  } = await queryAllKeynotes(client, {
    conference: process.env.conferenceCode,
    language: "it",
  });

  const {
    data: {
      conference: { keynotes: englishKeynotes },
    },
  } = await queryAllKeynotes(client, {
    conference: process.env.conferenceCode,
    language: "en",
  });

  const paths = [
    ...englishKeynotes.map((keynote) => ({
      params: {
        slug: keynote.slug,
      },
      locale: "en",
    })),
    ...italianKeynotes.map((keynote) => ({
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
