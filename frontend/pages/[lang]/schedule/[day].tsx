/** @jsx jsx */
import { useRouter } from "next/router";
import React, { Fragment } from "react";
import { DndProvider } from "react-dnd";
import Backend from "react-dnd-html5-backend";
import { FormattedMessage } from "react-intl";
import { Box, Flex, jsx } from "theme-ui";

import { useLoginState } from "~/app/profile/hooks";
import { formatDay } from "~/components/day-selector/format-day";
import { MetaTags } from "~/components/meta-tags";
import { ScheduleView } from "~/components/schedule-view";
import { useCurrentUser } from "~/helpers/use-current-user";

const Meta: React.SFC<{ day: string }> = ({ day }) => (
  <FormattedMessage id="schedule.pageTitle" values={{ day: formatDay(day) }}>
    {(text) => <MetaTags title={text} />}
  </FormattedMessage>
);

export const ScheduleDayPage = () => {
  const [loggedIn, _] = useLoginState();

  const router = useRouter();
  const day = router.query.day as string;

  const shouldFetchCurrentUser = loggedIn && router.query.admin !== undefined;
  const { user } = useCurrentUser({ skip: !shouldFetchCurrentUser });
  const shouldShowAdmin = user ? user.canEditSchedule : false;

  if (shouldShowAdmin) {
    return (
      <DndProvider backend={Backend}>
        <Meta day={day} />

        <ScheduleView day={day} shouldShowAdmin={shouldShowAdmin} />
      </DndProvider>
    );
  }

  return (
    <Fragment>
      <Meta day={day} />

      <ScheduleView day={day} shouldShowAdmin={shouldShowAdmin} />
    </Fragment>
  );
};

export default ScheduleDayPage;
