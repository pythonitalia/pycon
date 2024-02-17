/** @jsxRuntime classic */

/** @jsx jsx */
import { Separator, Spacer, Text } from "@python-italia/pycon-styleguide";
import { ArrowIcon, LiveIcon } from "@python-italia/pycon-styleguide/icons";
import clsx from "clsx";
import React, { Fragment, useEffect, useRef } from "react";
import { FormattedMessage } from "react-intl";
import useSyncScroll from "react-use-sync-scroll";
import { jsx, ThemeUIStyleObject } from "theme-ui";

import { useRouter } from "next/router";

import { isItemVisible } from ".";
import { ScheduleEntry } from "./events";
import { Placeholder } from "./placeholder";
import { Item, Room, Slot } from "./types";

const getSlotSize = (slot: Slot) => {
  if (["FREE_TIME", "BREAK"].includes(slot.type)) {
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
    (s) => convertHoursToMinutes(s.hour) + s.duration > end,
  );

  if (endingSlotIndex === -1) {
    endingSlotIndex = slots.length;
  }

  if (currentSlotIndex === endingSlotIndex) {
    // the item is shorter than the slot (e.g. we have a 30 mins talk in a 45 min slot)
    // we could calculate how much you actually use of the slot and set the size
    // to match the actual duration length, but in the UI it doesn't look good
    // as 30 of 45 is 0.6, so we use 0.9 to make it look better
    const sizeToNextSlot = slots
      .slice(currentSlotIndex, endingSlotIndex + 1)
      .reduce((acc, s) => acc + getSlotSize(s), 0);
    return {
      itemRowEnd: Math.floor(sizeToNextSlot * 0.85),
      sameSlotItem: true,
    };
  }

  return {
    itemRowEnd: slots
      .slice(currentSlotIndex, endingSlotIndex)
      .reduce((acc, s) => acc + getSlotSize(s), 0),
    sameSlotItem: false,
  };
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
  const { itemRowEnd, sameSlotItem } = getRowEnd({
    item,
    rowOffset,
    slot,
    slots,
  });
  const actualRowEnd = rowStart + itemRowEnd;

  const css: {
    gridColumnStart: number;
    gridColumnEnd: number;
    gridRowStart: number;
    gridRowEnd: number;
    borderBottom?: string;
  } = {
    gridColumnStart: index + 2,
    gridColumnEnd: index + 2 + item.rooms.length,
    gridRowStart: rowStart,
    gridRowEnd: actualRowEnd,
  };

  if (sameSlotItem) {
    css.borderBottom = "3px solid #000";
  }

  return css;
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
            "md:min-w-[2860px]": totalRooms > 3,
            "md:min-w-[100vw]": totalRooms <= 3,
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
  slots,
  rooms,
  currentDay,
  currentFilters,
  starredScheduleItems,
  toggleEventFavorite,
  liveSlot,
}: {
  slots: Slot[];
  rooms: Room[];
  currentFilters: Record<string, string[]>;
  toggleEventFavorite: (item: Item) => void;
  currentDay: string;
  starredScheduleItems: string[];
  liveSlot: Slot | null;
}) => {
  const rowOffset = 6;
  const totalRows = slots.reduce((count, slot) => count + getSlotSize(slot), 0);
  const totalColumns = rooms.length;
  const {
    query: { photo },
  } = useRouter();
  const isInPhotoMode = photo == "1";

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
            const isLive = slot.id === liveSlot?.id;
            const breakSlot = ["FREE_TIME", "BREAK"].includes(slot.type);

            rowStartPos = rowEnd;

            return (
              <Fragment key={slot.id}>
                {index > 0 && <Spacer showOnlyOn="mobile" size="xl" />}
                <div className="contents divide-y md:divide-none" key={slot.id}>
                  <div
                    className={clsx(
                      "md:border-r md:-mr-[3px] md:text-center md:px-4 left-0 sticky bg-milk z-40 pb-2",
                      {
                        "md:py-4": breakSlot,
                        "md:py-6": !breakSlot,
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
                      {isLive && (
                        <>
                          {!breakSlot && <Spacer size="xs" />}
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
                    />
                  ))}

                  {slot.items.map((item) => {
                    const starred = starredScheduleItems.includes(item.id);
                    return (
                      <ScheduleEntry
                        key={item.id}
                        item={item}
                        slot={slot}
                        rooms={rooms}
                        day={currentDay}
                        starred={starred}
                        filteredOut={
                          !isItemVisible(item, currentFilters, starred)
                        }
                        toggleEventFavorite={toggleEventFavorite}
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
                    );
                  })}

                  <div className="md:hidden"></div>
                </div>
              </Fragment>
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
