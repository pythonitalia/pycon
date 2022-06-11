/** @jsxRuntime classic */

/** @jsx jsx */
import React, { useState } from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { formatDay } from "~/components/day-selector/format-day";
import { MetaTags } from "~/components/meta-tags";
import { useLoginState } from "~/components/profile/hooks";
import { ScheduleView } from "~/components/schedule-view";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentUser } from "~/helpers/use-current-user";
import { useCurrentLanguage } from "~/locale/context";
import { Language } from "~/locale/languages";
import {
  querySchedule,
  queryScheduleDays,
  ScheduleQuery,
  useScheduleQuery,
} from "~/types";

const getDayUrl = (day: string) => `/schedule/${day}`;

const Meta: React.FC<{
  day: string;
  language: Language;
  timezone?: string;
}> = ({ day, language, timezone }) => (
  <FormattedMessage
    id="schedule.pageTitle"
    values={{ day: formatDay(day, language, timezone) }}
  >
    {(text) => <MetaTags title={text} />}
  </FormattedMessage>
);

export const ScheduleDayPage: React.FC = () => {
  const [loggedIn, _] = useLoginState();
  const code = process.env.conferenceCode;

  const router = useRouter();
  const day = router.query.day as string;
  const [currentDay, setCurrentDay] = useState(day);

  const shouldFetchCurrentUser = loggedIn && router.query.admin !== undefined;
  const { user } = useCurrentUser({ skip: !shouldFetchCurrentUser });
  const shouldShowAdmin = user ? user.canEditSchedule : false;

  const changeDay = (day: string) => {
    setCurrentDay(day);
    router.push("/schedule/[day]", getDayUrl(day), {
      shallow: true,
    });
  };

  const { loading, data } = useScheduleQuery({
    variables: {
      code,
      fetchSubmissions: shouldShowAdmin,
    },
  });

  if (shouldShowAdmin) {
    return (
      <DndProvider backend={HTML5Backend}>
        <PageContent
          loading={loading}
          shouldShowAdmin={shouldShowAdmin}
          data={data}
          day={currentDay}
          changeDay={changeDay}
        />
      </DndProvider>
    );
  }

  return (
    <PageContent
      loading={loading}
      shouldShowAdmin={shouldShowAdmin}
      data={data}
      day={currentDay}
      changeDay={changeDay}
    />
  );
};

type PageContentProps = {
  loading: boolean;
  shouldShowAdmin: boolean;
  data: ScheduleQuery;
  day: string;
  changeDay: (day: string) => void;
};

const PageContent: React.FC<PageContentProps> = ({
  loading,
  shouldShowAdmin,
  data,
  day,
  changeDay,
}) => {
  const language = useCurrentLanguage();

  return (
    <React.Fragment>
      <Meta
        day={day}
        language={language}
        timezone={data?.conference.timezone}
      />

      {loading && (
        <Box sx={{ borderTop: "primary" }}>
          <Box
            sx={{ maxWidth: "largeContainer", p: 3, mx: "auto", fontSize: 3 }}
          >
            <FormattedMessage id="schedule.loading" />
          </Box>
        </Box>
      )}
      {!loading && (
        <ScheduleView
          schedule={data}
          day={day}
          shouldShowAdmin={shouldShowAdmin}
          changeDay={changeDay}
        />
      )}
    </React.Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    querySchedule(client, {
      code: process.env.conferenceCode,
      fetchSubmissions: false,
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
