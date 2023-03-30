import {
  Section,
  Heading,
  Spacer,
  DaysSelector,
  Button,
  BasicButton,
  FilterBar,
  Text,
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
  const [currentFilters, setCurrentFilters] = useState({});
  const applyFilters = (newFilters: Record<string, string[]>) => {
    setCurrentFilters(newFilters);
  };
  const filters = [
    {
      id: "search",
      label: <FormattedMessage id="scheduleView.filter.search" />,
      search: true,
    },
    {
      id: "audienceLevel",
      label: <FormattedMessage id="scheduleView.filter.byAudience" />,
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        ...schedule.conference.audienceLevels.map((level) => ({
          label: level.name,
          value: level.id,
        })),
      ],
    },
    {
      id: "language",
      label: <FormattedMessage id="scheduleView.filter.byLanguage" />,
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        {
          label: <FormattedMessage id="global.english" />,
          value: "en",
        },
        {
          label: <FormattedMessage id="global.italian" />,
          value: "it",
        },
      ],
    },
    {
      id: "type",
      label: <FormattedMessage id="scheduleView.filter.byType" />,
      options: [
        {
          label: <FormattedMessage id="global.all" />,
          value: "",
        },
        {
          label: "Talk",
          value: "talk",
        },
        {
          label: "Workshop",
          value: "training",
        },
        {
          label: "Keynote",
          value: "keynote",
        },
        {
          label: "Panel",
          value: "panel",
        },
      ],
    },
  ];

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
          <div className="shrink-0 my-3 pl-4 md:pr-4 flex md:items-center md:justify-end">
            <span
              onClick={toggleScheduleView}
              className="cursor-pointer select-none"
            >
              <Text size="label3" uppercase weight="strong">
                {viewMode === "full" && (
                  <FormattedMessage id="schedule.mySchedule" />
                )}
                {viewMode === "personal" && (
                  <FormattedMessage id="schedule.fullSchedule" />
                )}
              </Text>
            </span>
            <div className="hidden md:block">
              <Spacer size="large" orientation="horizontal" />
            </div>
            <FilterBar
              placement="left"
              onApply={applyFilters}
              appliedFilters={currentFilters}
              filters={filters}
            />
          </div>
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
              currentFilters={currentFilters}
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
