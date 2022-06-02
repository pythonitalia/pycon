/** @jsxRuntime classic */

/** @jsx jsx */
import React, { useRef } from "react";
import useSyncScroll from "react-use-sync-scroll";
import { Box, jsx } from "theme-ui";

import { useRouter } from "next/router";

import { ScheduleEntry } from "./events";
import { isTraining } from "./is-training";
import { Placeholder } from "./placeholder";
import { Item, Room, Slot } from "./types";

const getSlotSize = (slot: Slot) => {
  if (slot.type === "FREE_TIME") {
    return 3;
  }
  return 12;
};

const fakeBottomBorder = {
  content: "''",
  display: "block",
  borderBottom: "primary",
  width: "100%",
  position: "absolute",
  bottom: "-4px",
  left: 0,
};

const fakeTopBorder = {
  ...fakeBottomBorder,
  borderBottom: "none",
  borderTop: "primary",
  bottom: "auto",
  top: "-4px",
};

const formatHour = (value: string) => {
  const [hour, minutes] = value.split(":");

  return [hour, minutes].join(".");
};

const convertHoursToMinutes = (value: string) => {
  const [hour, minutes] = value.split(":").map((x) => parseInt(x, 10));

  return hour * 60 + minutes;
};

const getRowEndForTraining = ({
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
  const duration = item.submission
    ? item.submission.duration!.duration
    : item.duration || 0;

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
  rowEnd,
}: {
  rowOffset: number;
  item: Item;
  slot: Slot;
  slots: Slot[];
  rooms: Room[];
  rowStart: number;
  rowEnd: number;
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

  if (isTraining(item)) {
    rowEnd = rowStart + getRowEndForTraining({ item, rowOffset, slot, slots });
  }

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
  }
>(({ totalColumns, totalRows, children, isInPhotoMode, ...props }, ref) => (
  <Box
    sx={{ width: "100%", overflow: "hidden", overflowX: "scroll" }}
    ref={ref}
    {...props}
  >
    <div
      sx={{
        minWidth: isInPhotoMode ? "100vw" : [null, "2000px"],
        gridTemplateColumns: `80px repeat(${totalColumns}, 1fr)`,
        gridTemplateRows: `repeat(${totalRows - 1}, 10px)`,
        py: "4px",
        backgroundColor: "black",
        gap: "4px",
        display: ["block", "grid"],
      }}
    >
      {children}
    </div>
  </Box>
));

export const Schedule: React.SFC<{
  slots: Slot[];
  rooms: Room[];
  adminMode: boolean;
  addCustomScheduleItem: (
    slotId: string,
    rooms: string[],
    title?: string,
  ) => void;
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
}> = ({
  adminMode,
  slots,
  rooms,
  addCustomScheduleItem,
  addSubmissionToSchedule,
  addKeynoteToSchedule,
  moveItem,
  currentDay,
}) => {
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
      addCustomScheduleItem(slot.id, roomIds, "Room Change");
    } else {
      const roomIds = item.event.allTracks
        ? rooms.map((room) => room.id)
        : [rooms[index].id];

      addCustomScheduleItem(slot.id, roomIds);
    }
  };

  const headerRef = useRef(null);
  const scheduleRef = useRef(null);

  const refsRef = useRef([headerRef, scheduleRef]);

  useSyncScroll(refsRef, { vertical: false, horizontal: true });

  let rowStartPos = 1;

  return (
    <React.Fragment>
      <GridContainer
        isInPhotoMode={isInPhotoMode}
        totalRows={rowOffset}
        totalColumns={totalColumns}
        ref={headerRef}
        sx={{
          position: "sticky",
          top: 0,
          zIndex: ["scheduleHeader"],
          overflowX: "hidden",
          mb: "-4px",
          display: ["none", "grid"],
        }}
      >
        <Box
          sx={{
            gridRowStart: 1,
            gridRowEnd: rowOffset,
            backgroundColor: "white",
          }}
        />
        {rooms.map((room, index) => (
          <Box
            key={index}
            sx={{
              gridColumnStart: "var(--column-start)",
              gridRowStart: 1,
              gridRowEnd: rowOffset,
              backgroundColor: "white",
              p: 2,
              fontSize: 1,
              fontWeight: "bold",
            }}
            style={
              {
                "--column-start": index + 2,
              } as any
            }
          >
            {room.name}
          </Box>
        ))}
      </GridContainer>

      <GridContainer
        isInPhotoMode={isInPhotoMode}
        ref={scheduleRef}
        totalRows={totalRows}
        totalColumns={totalColumns}
      >
        {slots
          .filter(
            (slot) =>
              !isInPhotoMode ||
              (isInPhotoMode && slot?.items[0]?.title !== "Registration"),
          )
          .map((slot) => {
            const rowStart = rowStartPos;
            const rowEnd = rowStartPos + getSlotSize(slot);

            rowStartPos = rowEnd;

            return (
              <div sx={{ display: "contents" }} key={slot.id}>
                <Box
                  sx={{
                    gridColumnStart: 1,
                    gridColumnEnd: 1,
                    gridRowStart: "var(--start)",
                    gridRowEnd: "var(--end)",
                    backgroundColor: "white",
                    p: [3, 2],
                    textAlign: [null, "center"],
                    fontWeight: "bold",
                  }}
                  style={
                    {
                      "--start": rowStart,
                      "--end": rowEnd,
                    } as any
                  }
                >
                  <Box>{formatHour(slot.hour)}</Box>
                </Box>

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

                {slot.items.map((item) => (
                  <ScheduleEntry
                    key={item.id}
                    item={item}
                    slot={slot}
                    rooms={rooms}
                    adminMode={adminMode}
                    day={currentDay}
                    sx={
                      {
                        position: "relative",
                        "&::before": fakeTopBorder,
                        "&::after": fakeBottomBorder,
                        ...getEntryPosition({
                          item,
                          rooms,
                          slot,
                          slots,
                          rowOffset,
                          rowStart,
                          rowEnd,
                        }),
                      } as any
                    }
                  />
                ))}
              </div>
            );
          })}
      </GridContainer>
    </React.Fragment>
  );
};
