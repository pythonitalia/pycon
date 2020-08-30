/** @jsx jsx */
import { useRouter } from "next/router";
import React, { Fragment } from "react";
import { DndProvider } from "react-dnd";
import Backend from "react-dnd-html5-backend";
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { useLoginState } from "~/app/profile/hooks";
import { formatDay } from "~/components/day-selector/format-day";
import { MetaTags } from "~/components/meta-tags";
import { ScheduleView } from "~/components/schedule-view";
import { useCurrentUser } from "~/helpers/use-current-user";
import { useCurrentLanguage } from "~/locale/context";
import { Language } from "~/locale/get-initial-locale";
import { ScheduleQuery, useScheduleQuery } from "~/types";

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

  const shouldFetchCurrentUser = loggedIn && router.query.admin !== undefined;
  const { user } = useCurrentUser({ skip: !shouldFetchCurrentUser });
  const shouldShowAdmin = user ? user.canEditSchedule : false;

  const { loading, data } = useScheduleQuery({
    variables: {
      code,
      fetchSubmissions: shouldShowAdmin,
    },
  });

  if (shouldShowAdmin) {
    return (
      <DndProvider backend={Backend}>
        <PageContent
          loading={loading}
          shouldShowAdmin={shouldShowAdmin}
          data={data}
          day={day}
        />
      </DndProvider>
    );
  }

  return (
    <PageContent
      loading={loading}
      shouldShowAdmin={shouldShowAdmin}
      data={data}
      day={day}
    />
  );
};

type PageContentProps = {
  loading: boolean;
  shouldShowAdmin: boolean;
  data: ScheduleQuery;
  day: string;
};

const PageContent: React.FC<PageContentProps> = ({
  loading,
  shouldShowAdmin,
  data,
  day,
}) => {
  const language = useCurrentLanguage();

  return (
    <>
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
        />
      )}
    </>
  );
};

export default ScheduleDayPage;
