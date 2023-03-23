import { Page } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { MetaTags } from "~/components/meta-tags";
import { ScheduleEventDetail } from "~/components/schedule-event-detail";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { queryAllKeynotes, queryKeynote, useKeynoteQuery } from "~/types";

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

  const [_, keynote] = await Promise.all([
    prefetchSharedQueries(client, locale),
    queryKeynote(client, {
      conference: process.env.conferenceCode,
      slug,
      language: locale,
    }),
  ]);

  if (!keynote.data || !keynote.data.conference.keynote) {
    return {
      notFound: true,
    };
  }

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
