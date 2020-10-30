/** @jsxRuntime classic */
/** @jsx jsx */
import React, { Fragment, useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Flex, Heading, jsx } from "theme-ui";

import { DaySelector } from "~/components/day-selector";
import {
  ScheduleQuery,
  useAddScheduleSlotMutation,
  useScheduleQuery,
  useUpdateOrCreateSlotItemMutation,
} from "~/types";

import { Button } from "../button/button";
import { Schedule } from "./schedule";
import { ItemsPanel } from "./staff/items-panel";

const LoadingOverlay = () => (
  <Flex
    sx={
      {
        position: "fixed",
        left: 0,
        right: 0,
        bottom: 0,
        top: 0,
        background: "rgba(0, 0, 0, 0.3)",
        zIndex: "scheduleLoading",
        alignItems: "center",
        justifyContent: "center",
      } as any
    }
  >
    <Box
      sx={{ backgroundColor: "white", border: "primary", p: 4, fontSize: 3 }}
    >
      Updating schedule, please wait...
    </Box>
  </Flex>
);

export const ScheduleView: React.SFC<{
  shouldShowAdmin: boolean;
  day?: string;
  schedule: ScheduleQuery;
}> = ({ day: currentDay, shouldShowAdmin, schedule }) => {
  const code = process.env.conferenceCode;

  const [addSlot, { loading: addingSlot }] = useAddScheduleSlotMutation({
    variables: { code, day: currentDay, duration: 60 },
  });

  const [
    addOrCreateScheduleItem,
    { loading: updatingSchedule },
  ] = useUpdateOrCreateSlotItemMutation();

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

  const { rooms, days, submissions } = schedule.conference!;
  const day = days.find((d) => d.day === currentDay);

  return (
    <Fragment>
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
                timezone={schedule.conference.timezone}
              />
            </Box>
          </Box>
        </Box>

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
            {schedule.conference.durations.map((duration) => {
              if (
                duration.allowedSubmissionTypes.find(
                  (type) => type.name.toLowerCase() !== "talk",
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
