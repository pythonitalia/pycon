/** @jsx jsx */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Button, Flex, Heading } from "@theme-ui/components";
import { navigate } from "gatsby";
import React, { Fragment, useCallback, useLayoutEffect, useState } from "react";
import { DndProvider } from "react-dnd";
import Backend from "react-dnd-html5-backend";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "../../app/profile/hooks";
import { MetaTags } from "../../components/meta-tags";
import { useConference } from "../../context/conference";
import { useCurrentLanguage } from "../../context/language";
import {
  AddScheduleSlotMutation,
  AddScheduleSlotMutationVariables,
  ScheduleQuery,
  ScheduleQueryVariables,
  UpdateOrCreateSlotItemMutation,
  UpdateOrCreateSlotItemMutationVariables,
} from "../../generated/graphql-backend";
import { useCurrentUser } from "../../helpers/use-current-user";
import ADD_SCHEDULE_SLOT_QUERY from "./add-schedule-slot.graphql";
import { DaySelector } from "./day-selector";
import { formatDay } from "./format-day";
import { Schedule } from "./schedule";
import SCHEDULE_QUERY from "./schedule.graphql";
import { ItemsPanel } from "./staff/items-panel";
import UPDATE_OR_CREATE_ITEM from "./update-or-create-item.graphql";

const LoadingOverlay = () => (
  <Flex
    sx={{
      position: "fixed",
      left: 0,
      right: 0,
      bottom: 0,
      top: 0,
      background: "rgba(0, 0, 0, 0.3)",
      zIndex: "scheduleLoading",
      alignItems: "center",
      justifyContent: "center",
    }}
  >
    <Box
      sx={{ backgroundColor: "white", border: "primary", p: 4, fontSize: 3 }}
    >
      Updating schedule, please wait...
    </Box>
  </Flex>
);

const Meta: React.SFC<{ day: string }> = ({ day }) => (
  <FormattedMessage id="schedule.pageTitle" values={{ day: formatDay(day) }}>
    {text => <MetaTags title={text} />}
  </FormattedMessage>
);

export const ScheduleScreen: React.SFC<RouteComponentProps<{
  day: string;
}>> = ({ day: dayParam, location }) => {
  const [loggedIn, _] = useLoginState();

  const shouldFetchCurrentUser = loggedIn && location?.search.includes("admin");
  const { user } = useCurrentUser({ skip: !shouldFetchCurrentUser });
  const shouldShowAdmin = user ? user.canEditSchedule : false;

  if (shouldShowAdmin) {
    return (
      <DndProvider backend={Backend}>
        <ScheduleView day={dayParam} shouldShowAdmin={shouldShowAdmin} />
      </DndProvider>
    );
  }

  return <ScheduleView day={dayParam} shouldShowAdmin={shouldShowAdmin} />;
};

export const ScheduleView: React.SFC<{
  shouldShowAdmin: boolean;
  day?: string;
}> = ({ day: dayParam, shouldShowAdmin }) => {
  const { code } = useConference();
  const currentDay = dayParam!;

  const language = useCurrentLanguage();

  const setCurrentDay = useCallback(
    (d: string) => navigate(`/${language}/schedule/${d}`),
    [],
  );

  const { loading, data, error } = useQuery<
    ScheduleQuery,
    ScheduleQueryVariables
  >(SCHEDULE_QUERY, {
    variables: {
      code,
      fetchSubmissions: shouldShowAdmin,
    },
  });

  const [addSlot, { loading: addingSlot }] = useMutation<
    AddScheduleSlotMutation,
    AddScheduleSlotMutationVariables
  >(ADD_SCHEDULE_SLOT_QUERY, {
    variables: { code, day: currentDay, duration: 60 },
  });

  const [addOrCreateScheduleItem, { loading: updatingSchedule }] = useMutation<
    UpdateOrCreateSlotItemMutation,
    UpdateOrCreateSlotItemMutationVariables
  >(UPDATE_OR_CREATE_ITEM);

  const addCustomScheduleItem = useCallback(
    (slotId: string, itemRooms: string[]) =>
      addOrCreateScheduleItem({
        variables: {
          input: {
            slotId,
            rooms: itemRooms,
            title: "Custom",
          },
        },
      }),
    [],
  );

  const addSubmissionToSchedule = useCallback(
    (slotId: string, itemRooms: string[], submissionId: string) =>
      addOrCreateScheduleItem({
        variables: {
          input: {
            slotId,
            submissionId,
            rooms: itemRooms,
          },
        },
      }),
    [],
  );

  const moveItem = useCallback(
    (slotId: string, itemRooms: string[], itemId: string) =>
      addOrCreateScheduleItem({
        variables: {
          input: {
            slotId,
            itemId,
            rooms: itemRooms,
          },
        },
      }),
    [],
  );

  const addScheduleSlot = useCallback(
    (duration: number) =>
      addSlot({
        variables: {
          code,
          day: currentDay,
          duration,
        },
      }),
    [code, currentDay],
  );

  useLayoutEffect(() => {
    if (!currentDay && data?.conference) {
      setCurrentDay(data.conference.days[0].day);
    }
  }, [data]);

  if (error) {
    throw error;
  }

  const { rooms, days, submissions } = loading
    ? { rooms: [], days: [], submissions: [] }
    : data?.conference!;

  const day = days.find(d => d.day === currentDay);

  return (
    <Fragment>
      <Meta day={currentDay} />

      {shouldShowAdmin && <ItemsPanel submissions={submissions!} />}
      {(addingSlot || updatingSchedule) && <LoadingOverlay />}
      <Box
        sx={{ flex: 1, width: shouldShowAdmin ? "calc(100% - 300px)" : "100%" }}
      >
        <Box sx={{ backgroundColor: "orange", borderTop: "primary" }}>
          <Box
            sx={{
              display: ["block", null, "flex"],
              py: 4,
              px: 3,
              maxWidth: "largeContainer",
              mx: "auto",
            }}
          >
            <Heading sx={{ fontSize: 6 }}>Schedule</Heading>

            <Box sx={{ ml: "auto" }}>
              <DaySelector
                days={days}
                currentDay={currentDay}
                setCurrentDay={setCurrentDay}
              />
            </Box>
          </Box>
        </Box>

        {loading && (
          <Box sx={{ borderTop: "primary" }}>
            <Box
              sx={{ maxWidth: "largeContainer", p: 3, mx: "auto", fontSize: 3 }}
            >
              <FormattedMessage id="schedule.loading" />
            </Box>
          </Box>
        )}

        {day && (
          <Schedule
            slots={day.slots}
            rooms={rooms}
            adminMode={shouldShowAdmin}
            addCustomScheduleItem={addCustomScheduleItem}
            addSubmissionToSchedule={addSubmissionToSchedule}
            moveItem={moveItem}
          />
        )}

        {shouldShowAdmin && (
          <Box sx={{ my: 4, ml: 100 }}>
            {data?.conference.durations.map(duration => {
              if (
                duration.allowedSubmissionTypes.find(
                  type => type.name.toLowerCase() !== "talk",
                )
              ) {
                return null;
              }

              return (
                <Button
                  sx={{ mr: 3 }}
                  key={duration.duration}
                  onClick={() => addScheduleSlot(duration.duration)}
                >
                  Add {duration.duration} minutes slot
                </Button>
              );
            })}
          </Box>
        )}
      </Box>
    </Fragment>
  );
};
