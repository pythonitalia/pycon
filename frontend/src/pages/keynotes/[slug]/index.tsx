/** @jsxRuntime classic */

/** @jsx jsx */
import { Page } from "@python-italia/pycon-styleguide";
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
import { ScheduleEventDetail } from "~/components/schedule-event-detail";
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
    query: { slug },
  } = useRouter();
  const {
    data: {
      conference: {
        keynote: { title, description, speakers, start, end },
      },
    },
  } = useKeynoteQuery({
    variables: {
      conference: process.env.conferenceCode,
      slug: slug as string,
      language,
    },
  });

  const speakersName = speakers.map((speaker) => speaker.fullName).join(" & ");

  return (
    <Page endSeparator={false}>
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

      <ScheduleEventDetail
        type="keynote"
        eventTitle={title}
        abstract={description}
        language="en"
        startTime={start}
        endTime={end}
        bookable={false}
        speakers={speakers.map((speaker) => ({
          name: speaker.fullName,
          photo: speaker.participant.photo,
          bio: speaker.participant.bio,
          twitterHandle: speaker.participant.twitterHandle,
          instagramHandle: speaker.participant.instagramHandle,
          linkedinUrl: speaker.participant.linkedinUrl,
          facebookUrl: speaker.participant.facebookUrl,
          mastodonHandle: speaker.participant.mastodonHandle,
        }))}
      />
    </Page>
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
