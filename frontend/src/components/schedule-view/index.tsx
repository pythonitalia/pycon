import {
  Section,
  Heading,
  Spacer,
  DaysSelector,
  Button,
  BasicButton,
} from "@python-italia/pycon-styleguide";
import React, { Fragment, useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";

import { useRouter } from "next/router";

import { useCurrentLanguage } from "~/locale/context";
import {
  ScheduleQuery,
  useAddScheduleSlotMutation,
  useUpdateOrCreateSlotItemMutation,
} from "~/types";

import { Schedule } from "./schedule";
import { ItemsPanel } from "./staff/items-panel";

export type ViewMode = "full" | "personal";

const LoadingOverlay = () => (
  <div className="flex fixed inset-0 bg-black/30 z-10 items-center justify-center">
    <div className="bg-white border p-4">Updating schedule, please wait...</div>
  </div>
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
  const [viewMode, setViewMode] = useState<ViewMode>("full");

  const [addSlot, { loading: addingSlot }] = useAddScheduleSlotMutation({
    variables: { code, day: currentDay, duration: 60, language },
  });

  const [addOrCreateScheduleItem, { loading: updatingSchedule }] =
    useUpdateOrCreateSlotItemMutation();

  const toggleScheduleView = useCallback(() => {
    setViewMode((current) => (current === "full" ? "personal" : "full"));
  }, []);

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
      {!isInPhotoMode && (
        <>
          <Section illustration="snakeHead">
            <Heading size="display1">Schedule</Heading>
          </Section>
        </>
      )}

      <Section noContainer>
        <DaysSelector
          days={days.map((d) => ({
            date: d.day,
            selected: d.day === currentDay,
          }))}
          onClick={changeDay}
          language={language}
        >
          <BasicButton onClick={toggleScheduleView}>
            {viewMode === "full" && (
              <FormattedMessage id="schedule.mySchedule" />
            )}
            {viewMode === "personal" && (
              <FormattedMessage id="schedule.fullSchedule" />
            )}
          </BasicButton>
        </DaysSelector>
        <Spacer size="large" />

        {day && (
          <div>
            <Schedule
              viewMode={viewMode}
              slots={day.slots}
              rooms={day.rooms}
              adminMode={shouldShowAdmin}
              addCustomScheduleItem={addCustomScheduleItem}
              addSubmissionToSchedule={addSubmissionToSchedule}
              addKeynoteToSchedule={addKeynoteToSchedule}
              moveItem={moveItem}
              currentDay={currentDay}
            />
          </div>
        )}

        {shouldShowAdmin && (
          <div className="my-4 ml-24">
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
                  key={duration.duration}
                  onClick={() => addScheduleSlot(duration.duration)}
                >
                  Add {duration.duration} minutes slot
                </Button>
              );
            })}
          </div>
        )}
      </Section>
    </Fragment>
  );
};
