/** @jsxRuntime classic */

/** @jsx jsx */
import { Separator, Spacer, Text } from "@python-italia/pycon-styleguide";
import { ArrowIcon, LiveIcon } from "@python-italia/pycon-styleguide/icons";
import clsx from "clsx";
import { isAfter, isBefore, parseISO } from "date-fns";
import React, { useEffect, useRef, useState } from "react";
import { FormattedMessage } from "react-intl";
import useSyncScroll from "react-use-sync-scroll";
import { jsx, ThemeUIStyleObject } from "theme-ui";

import { useRouter } from "next/router";

import { useUserStarredScheduleItemsQuery } from "~/types";

import { ViewMode } from ".";
import { useLoginState } from "../profile/hooks";
import { ScheduleEntry } from "./events";
import { isTraining } from "./is-training";
import { Placeholder } from "./placeholder";
import { Item, ItemTypes, Room, Slot } from "./types";

const getSlotSize = (slot: Slot) => {
  if (slot.type === "FREE_TIME") {
    return 5;
  }
  return 31;
};

const formatHour = (value: string) => {
  const [hour, minutes] = value.split(":");

  return [hour, minutes].join(".");
};

const convertHoursToMinutes = (value: string) => {
  const [hour, minutes] = value.split(":").map((x) => parseInt(x, 10));

  return hour * 60 + minutes;
};

const getRowEnd = ({
  item,
  rowOffset,
  slot,
  slots,
}: {
  item: Item;
  rowOffset: number;
  slot: Slot;
  slots: Slot[];
}) => {
  const start = convertHoursToMinutes(slot.hour);
  const duration =
    item.duration || slot.duration || item.submission?.duration?.duration;

  const end = start + duration;

  const currentSlotIndex = slots.findIndex((s) => s.id === slot.id);

  let endingSlotIndex = slots.findIndex(
    (s) => convertHoursToMinutes(s.hour) + s.duration >= end,
  );

  if (endingSlotIndex === -1) {
    endingSlotIndex = slots.length - 1;
  }

  return slots
    .slice(currentSlotIndex, endingSlotIndex + 1)
    .reduce((acc, s) => acc + getSlotSize(s), 0);
};

const getEntryPosition = ({
  item,
  rooms,
  slot,
  slots,
  rowOffset,
  rowStart,
}: {
  rowOffset: number;
  item: Item;
  slot: Slot;
  slots: Slot[];
  rooms: Room[];
  rowStart: number;
}) => {
  // find all the indexes for the rooms of this item, then
  // sort them and use the first one for the index of the item
  // this allows us to have items on multiple rooms without having
  // to use complex logic to understand where to position them, as
  // we now assume that the rooms are always consecutive
  const roomIndexes = item.rooms
    .map((room) => rooms.findIndex((r) => r.id === room.id))
    .sort();

  const index = roomIndexes[0];
  const rowEnd = rowStart + getRowEnd({ item, rowOffset, slot, slots });

  return {
    gridColumnStart: index + 2,
    gridColumnEnd: index + 2 + item.rooms.length,
    gridRowStart: rowStart,
    gridRowEnd: rowEnd,
  };
};

const GridContainer = React.forwardRef<
  null,
  {
    totalColumns: number;
    totalRows: number;
    isInPhotoMode: boolean;
    children: React.ReactNode;
    sx?: ThemeUIStyleObject;
    className?: string;
    totalRooms: number;
  }
>(
  (
    {
      totalColumns,
      totalRows,
      children,
      isInPhotoMode,
      className,
      totalRooms,
      ...props
    },
    ref,
  ) => (
    <div
      className={clsx("w-full overflow-hidden overflow-x-scroll", className)}
      ref={ref}
      {...props}
    >
      <div
        className={clsx(
          "bg-milk md:bg-black px-4 md:px-0 block md:grid gap-[3px] py-[3px]",
          {
            "md:min-w-[2860px]": totalRooms > 2,
            "md:min-w-[100vw]": totalRooms <= 2,
          },
        )}
        style={{
          gridTemplateColumns: `128px repeat(${totalColumns}, 1fr)`,
          gridTemplateRows: `repeat(${totalRows - 1}, 10px)`,
        }}
      >
        {children}
      </div>
    </div>
  ),
);

export const Schedule = ({
  adminMode,
  slots,
  rooms,
  addCustomScheduleItem,
  addSubmissionToSchedule,
  addKeynoteToSchedule,
  moveItem,
  currentDay,
  viewMode,
}: {
  slots: Slot[];
  rooms: Room[];
  adminMode: boolean;
  addCustomScheduleItem: (
    slotId: string,
    rooms: string[],
    title?: string,
  ) => void;
  viewMode: ViewMode;
  moveItem: (slotId: string, rooms: string[], itemId: string) => void;
  addSubmissionToSchedule: (
    slotId: string,
    rooms: string[],
    submissionId: string,
  ) => void;
  addKeynoteToSchedule: (
    slotId: string,
    rooms: string[],
    keynoteId: string,
  ) => void;
  currentDay: string;
}) => {
  const [loggedIn] = useLoginState();
  const [liveSlot, setLiveSlot] = useState<string | undefined>(
    findLiveSlot({ currentDay, slots })?.id,
  );
  const { data: { me: { starredScheduleItems = [] } = {} } = {} } =
    useUserStarredScheduleItemsQuery({
      skip: !loggedIn,
      variables: {
        code: process.env.conferenceCode,
      },
    });

  const rowOffset = 6;
  const totalRows = slots.reduce((count, slot) => count + getSlotSize(slot), 0);
  const totalColumns = rooms.length;
  const {
    query: { photo },
  } = useRouter();
  const isInPhotoMode = photo == "1";

  const handleDrop = (item: any, slot: Slot, index: number) => {
    if (item.itemId) {
      moveItem(slot.id, [rooms[index].id], item.itemId);
    } else if (item.event.submissionId) {
      addSubmissionToSchedule(
        slot.id,
        [rooms[index].id],
        item.event.submissionId,
      );
    } else if (item.event.keynoteId) {
      addKeynoteToSchedule(
        slot.id,
        rooms.filter((room) => room.type !== "training").map((room) => room.id),
        item.event.keynoteId,
      );
    } else if (item.event.roomChange) {
      const roomIds = rooms
        .filter((room) => room.type !== "training")
        .map((room) => room.id);
      addCustomScheduleItem(slot.id, roomIds, "Room Change / Cambio stanza");
    } else {
      const roomIds = item.event.allTracks
        ? rooms.map((room) => room.id)
        : [rooms[index].id];

      addCustomScheduleItem(slot.id, roomIds);
    }
  };

  const headerRef = useRef(null);
  const scheduleRef = useRef(null);

  const scrollScheduleBack = () => {
    scheduleRef.current.scrollBy({
      left: -300,
      behavior: "smooth",
    });
  };
  const scrollScheduleForward = () => {
    scheduleRef.current.scrollBy({
      left: 300,
      behavior: "smooth",
    });
  };

  useEffect(() => {
    scheduleRef.current.scroll({
      left: 0,
    });
  }, [currentDay]);

  useEffect(() => {
    const listener = () => {
      if (!document.hidden) {
        const liveSlot = findLiveSlot({ currentDay, slots });

        if (liveSlot) {
          setLiveSlot(liveSlot.id);
        }
      }
    };
    document.addEventListener("visibilitychange", listener);

    return () => {
      document.removeEventListener("visibilitychange", listener);
    };
  }, []);

  const refsRef = useRef([headerRef, scheduleRef]);

  useSyncScroll(refsRef, { vertical: false, horizontal: true });

  let rowStartPos = 1;

  const totalRooms = rooms.length;

  return (
    <React.Fragment>
      <GridContainer
        isInPhotoMode={isInPhotoMode}
        totalRows={rowOffset}
        totalColumns={totalColumns}
        ref={headerRef}
        totalRooms={totalRooms}
        className="hidden md:grid sticky top-0 overflow-x-hidden -mb-[3px] no-scrollbar z-50"
      >
        <div
          sx={{
            gridRowStart: 1,
            gridRowEnd: rowOffset,
            backgroundColor: "#FAF5F3",
            position: "sticky",
            left: 0,
            zIndex: "scheduleTimes",
            borderRight: "primary",
            marginRight: "-3px",
            overflow: "hidden",
            display: "grid",
            gridTemplateColumns: "1fr auto 1fr",
          }}
        >
          <ArrowControl reverse onClick={scrollScheduleBack} />
          <Separator orientation="vertical" />
          <ArrowControl onClick={scrollScheduleForward} />
        </div>
        {rooms.map((room, index) => (
          <div
            key={index}
            sx={
              {
                gridColumnStart: "var(--column-start)",
                gridRowStart: 1,
                gridRowEnd: rowOffset,
                backgroundColor: "#FAF5F3",
                padding: 24,
                fontSize: 1,
                fontWeight: "bold",
                "--column-start": index + 2,
                display: "flex",
                alignItems: "center",
              } as any
            }
          >
            <Text uppercase size="label3" weight="strong">
              {room.name}
            </Text>
          </div>
        ))}
      </GridContainer>

      <GridContainer
        isInPhotoMode={isInPhotoMode}
        ref={scheduleRef}
        totalRows={totalRows}
        totalColumns={totalColumns}
        totalRooms={totalRooms}
      >
        {slots
          .filter(
            (slot) =>
              !isInPhotoMode ||
              (isInPhotoMode && slot?.items[0]?.title !== "Registration"),
          )
          .map((slot, index) => {
            const rowStart = rowStartPos;
            const rowEnd = rowStartPos + getSlotSize(slot);
            const isLive = slot.id === liveSlot;
            const freeTimeSlot = slot.type === "FREE_TIME";

            rowStartPos = rowEnd;

            return (
              <>
                {index > 0 && <Spacer showOnlyOn="mobile" size="xl" />}
                <div className="contents divide-y md:divide-none" key={slot.id}>
                  <div
                    className={clsx(
                      "md:border-r md:-mr-[3px] md:text-center md:px-4 left-0 sticky bg-milk z-40 pb-2",
                      {
                        "md:py-4": freeTimeSlot,
                        "md:py-6": !freeTimeSlot,
                        "md:bg-coral": isLive,
                      },
                    )}
                    style={
                      {
                        gridColumnStart: 1,
                        gridColumnEnd: 1,
                        gridRowStart: "var(--start)",
                        gridRowEnd: "var(--end)",
                        "--start": rowStart,
                        "--end": rowEnd,
                      } as any
                    }
                  >
                    <Text weight="strong" size="label1" className="md:hidden">
                      <FormattedMessage
                        id="schedule.time"
                        values={{
                          start: formatHour(slot.hour),
                          end: formatHour(slot.endHour),
                        }}
                      />

                      {isLive && (
                        <>
                          <Spacer size="small" orientation="horizontal" />
                          <LiveIcon className="inline-block" />
                        </>
                      )}
                    </Text>
                    <Text
                      weight="strong"
                      size="label1"
                      className="hidden md:block"
                    >
                      <FormattedMessage
                        id="schedule.timeNoEnd"
                        values={{
                          start: formatHour(slot.hour),
                        }}
                      />
                      {slot.id === liveSlot && (
                        <>
                          {!freeTimeSlot && <Spacer size="xs" />}
                          <Text as="p" uppercase size="label3" weight="strong">
                            <FormattedMessage id="schedule.live" />
                          </Text>
                        </>
                      )}
                    </Text>
                  </div>

                  {rooms.map((room, index) => (
                    <Placeholder
                      key={`${room.id}-${slot.id}`}
                      columnStart={index + 2}
                      rowStart={rowStart}
                      rowEnd={rowEnd}
                      duration={slot.duration}
                      roomType={room.type}
                      adminMode={adminMode}
                      onDrop={(item: any) => handleDrop(item, slot, index)}
                    />
                  ))}

                  {slot.items
                    .filter((item) => {
                      if (
                        viewMode === "personal" &&
                        item.type !== "custom" &&
                        !starredScheduleItems.includes(item.id)
                      ) {
                        return false;
                      }

                      return true;
                    })
                    .map((item) => (
                      <ScheduleEntry
                        key={item.id}
                        item={item}
                        slot={slot}
                        rooms={rooms}
                        adminMode={adminMode}
                        day={currentDay}
                        starred={starredScheduleItems.includes(item.id)}
                        style={
                          {
                            position: "relative",
                            ...getEntryPosition({
                              item,
                              rooms,
                              slot,
                              slots,
                              rowOffset,
                              rowStart,
                            }),
                          } as any
                        }
                      />
                    ))}

                  <div className="md:hidden"></div>
                </div>
              </>
            );
          })}
      </GridContainer>
    </React.Fragment>
  );
};

type ArrowControlProps = {
  reverse?: boolean;
  onClick: () => void;
};

const ArrowControl = ({ reverse, onClick }: ArrowControlProps) => {
  return (
    <div
      onClick={onClick}
      className={clsx("bg-cream p-4 cursor-pointer select-none", {
        "rotate-180": reverse,
      })}
    >
      <ArrowIcon />
    </div>
  );
};

const findLiveSlot = ({
  currentDay,
  slots,
}: {
  currentDay: string;
  slots: Slot[];
}): Slot | undefined => {
  const now = new Date();
  return slots.find((slot) => {
    const startHour = parseISO(`${currentDay}T${slot.hour}`);
    const endHour = parseISO(`${currentDay}T${slot.endHour}`);

    return isAfter(now, startHour) && isBefore(now, endHour);
  });
};
