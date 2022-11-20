/** @jsxRuntime classic */

/** @jsx jsx */
import React, { Fragment, useCallback } from "react";
import { Box, Flex, Heading, jsx } from "theme-ui";

import { useRouter } from "next/router";

import { DaySelector } from "~/components/day-selector";
import { useCurrentLanguage } from "~/locale/context";
import {
  ScheduleQuery,
  useAddScheduleSlotMutation,
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

export const ScheduleView = ({
  day: currentDay,
  shouldShowAdmin,
  schedule,
  changeDay,
}: {
  shouldShowAdmin: boolean;
  day?: string;
  schedule: ScheduleQuery;
  changeDay: (day: string) => void;
}) => {
  const language = useCurrentLanguage();
  const code = process.env.conferenceCode;
  const {
    query: { photo },
  } = useRouter();
  const isInPhotoMode = photo == "1";

  const [addSlot, { loading: addingSlot }] = useAddScheduleSlotMutation({
    variables: { code, day: currentDay, duration: 60, language },
  });

  const [
    addOrCreateScheduleItem,
    { loading: updatingSchedule },
  ] = useUpdateOrCreateSlotItemMutation();

  const addCustomScheduleItem = useCallback(
    (slotId: string, itemRooms: string[], title = "Custom") =>
      addOrCreateScheduleItem({
        variables: {
          input: {
            slotId,
            rooms: itemRooms,
            title,
          },
          language,
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
          language,
        },
      }),
    [],
  );

  const addKeynoteToSchedule = useCallback(
    (slotId: string, itemRooms: string[], keynoteId: string) =>
      addOrCreateScheduleItem({
        variables: {
          input: {
            slotId,
            keynoteId,
            rooms: itemRooms,
          },
          language,
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
          language,
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
          language,
        },
      }),
    [code, currentDay],
  );

  const { days, submissions, keynotes } = schedule.conference!;
  const day = days.find((d) => d.day === currentDay);

  return (
    <Fragment>
      {shouldShowAdmin && (
        <ItemsPanel keynotes={keynotes ?? []} submissions={submissions ?? []} />
      )}
      {(addingSlot || updatingSchedule) && <LoadingOverlay />}
      <Box
        sx={{ flex: 1, width: shouldShowAdmin ? "calc(100% - 300px)" : "100%" }}
      >
        {!isInPhotoMode && (
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
                  changeDay={changeDay}
                />
              </Box>
            </Box>
          </Box>
        )}

        {day && (
          <Schedule
            slots={day.slots}
            rooms={day.rooms}
            adminMode={shouldShowAdmin}
            addCustomScheduleItem={addCustomScheduleItem}
            addSubmissionToSchedule={addSubmissionToSchedule}
            addKeynoteToSchedule={addKeynoteToSchedule}
            moveItem={moveItem}
            currentDay={currentDay}
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
