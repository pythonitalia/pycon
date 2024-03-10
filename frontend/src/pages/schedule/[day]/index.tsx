import { stringify } from "querystring";
import { Page } from "@python-italia/pycon-styleguide";
import React, { useState } from "react";
import { FormattedMessage } from "react-intl";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { ScheduleView } from "~/components/schedule-view";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentUser } from "~/helpers/use-current-user";
import { useCurrentLanguage } from "~/locale/context";
import { Language } from "~/locale/languages";
import {
  ScheduleQuery,
  querySchedule,
  queryScheduleDays,
  useScheduleQuery,
} from "~/types";

export const getDayUrl = (day: string, language: Language | null = null) => {
  if (language) {
    return `/${language}/schedule/${day}`;
  }
  return `/schedule/${day}`;
};

export const formatDay = (
  day: string,
  language: Language,
  timezone: string,
) => {
  const d = new Date(day);
  const formatter = new Intl.DateTimeFormat(language, {
    weekday: "long",
    day: "numeric",
    timeZone: timezone,
  });
  return formatter.format(d);
};

const Meta = ({
  day,
  language,
  timezone,
}: {
  day: string;
  language: Language;
  timezone?: string;
}) => (
  <FormattedMessage
    id="schedule.pageTitle"
    values={{ day: formatDay(day, language, timezone) }}
  >
    {(text) => <MetaTags title={text} />}
  </FormattedMessage>
);

export const ScheduleDayPage = () => {
  const [loggedIn, _] = useLoginState();
  const code = process.env.conferenceCode;
  const language = useCurrentLanguage();

  const router = useRouter();
  const day = router.query.day as string;
  const [currentDay, setCurrentDay] = useState(day);

  const { user } = useCurrentUser({ skip: !loggedIn });

  const changeDay = (day: string) => {
    setCurrentDay(day);
    const url = getDayUrl(day);
    router.push(`${url}?${stringify(router.query)}`, undefined, {
      shallow: true,
    });
  };

  const { data } = useScheduleQuery({
    variables: {
      code,
      language,
    },
  });

  return <PageContent data={data} day={currentDay} changeDay={changeDay} />;
};

type PageContentProps = {
  data: ScheduleQuery;
  day: string;
  changeDay: (day: string) => void;
};

const PageContent = ({ data, day, changeDay }: PageContentProps) => {
  const language = useCurrentLanguage();

  return (
    <Page endSeparator={false}>
      <Meta
        day={day}
        language={language}
        timezone={data?.conference.timezone}
      />

      <ScheduleView schedule={data} day={day} changeDay={changeDay} />
    </Page>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    querySchedule(client, {
      code: process.env.conferenceCode,
      language: locale,
    }),
  ]);

  return addApolloState(
    client,
    {
      props: {},
    },
    60,
  );
};

export const getStaticPaths: GetStaticPaths = async () => {
  const client = getApolloClient();

  const {
    data: {
      conference: { days },
    },
  } = await queryScheduleDays(client, {
    code: process.env.conferenceCode,
  });

  const paths = [
    ...days.map((day) => ({
      params: {
        day: day.day,
      },
      locale: "en",
    })),
    ...days.map((day) => ({
      params: {
        day: day.day,
      },
      locale: "it",
    })),
  ];

  return {
    paths,
    fallback: "blocking",
  };
};

export default ScheduleDayPage;
