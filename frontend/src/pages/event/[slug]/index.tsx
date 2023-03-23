import { Page } from "@python-italia/pycon-styleguide";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { MetaTags } from "~/components/meta-tags";
import { ScheduleEventDetail } from "~/components/schedule-event-detail";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { queryAllTalks, queryTalk, useTalkQuery } from "~/types";

export const TalkPage = () => {
  const router = useRouter();
  const slug = router.query.slug as string;
  const language = useCurrentLanguage();
  const { data } = useTalkQuery({
    returnPartialData: true,
    variables: {
      code: process.env.conferenceCode,
      slug,
      language,
    },
  });

  const { talk } = data.conference;

  const description = talk.submission
    ? talk.submission.abstract
    : talk.description;

  return (
    <Page endSeparator={false}>
      <MetaTags title={talk.title} useDefaultSocialCard={false} />

      <ScheduleEventDetail
        id={talk.id}
        slug={slug}
        type={getType(talk.type)}
        eventTitle={talk.title}
        elevatorPitch={talk.submission?.elevatorPitch}
        abstract={description}
        tags={talk.submission?.tags.map((tag) => tag.name)}
        language={talk.language.code}
        audienceLevel={talk.submission?.audienceLevel.name}
        startTime={talk.start}
        endTime={talk.end}
        speakers={talk.speakers.map((speaker) => ({
          name: speaker.fullName,
          photo: speaker.participant?.photo,
          bio: speaker.participant?.bio,
          twitterHandle: speaker.participant?.twitterHandle,
          instagramHandle: speaker.participant?.instagramHandle,
          linkedinUrl: speaker.participant?.linkedinUrl,
          facebookUrl: speaker.participant?.facebookUrl,
          mastodonHandle: speaker.participant?.mastodonHandle,
          website: speaker.participant?.website,
        }))}
        bookable={talk.hasLimitedCapacity}
        spacesLeft={talk.spacesLeft}
      />
    </Page>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale, params }) => {
  const slug = params.slug as string;
  const client = getApolloClient();

  const [_, event] = await Promise.all([
    prefetchSharedQueries(client, locale),
    queryTalk(client, {
      code: process.env.conferenceCode,
      slug,
      language: locale,
    }),
  ]);

  if (!event.data || !event.data.conference.talk) {
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
      conference: { talks },
    },
  } = await queryAllTalks(client, {
    code: process.env.conferenceCode,
  });

  const paths = [
    ...talks.map((talk) => ({
      params: {
        slug: talk.slug,
      },
      locale: "en",
    })),
    ...talks.map((talk) => ({
      params: {
        slug: talk.slug,
      },
      locale: "it",
    })),
  ];

  return {
    paths,
    fallback: "blocking",
  };
};

const getType = (
  type: string,
): Parameters<typeof ScheduleEventDetail>[0]["type"] => {
  switch (type.toLowerCase()) {
    case "workshop":
    case "tutorial":
    case "training":
      return "workshop";
    case "talk":
      return "talk";
    case "panel":
      return "panel";
  }
};

export default TalkPage;
