/** @jsx jsx */
import { Box, Grid } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

import { ScheduleEntry } from "./events";
import { isTraining } from "./is-training";
import { Placeholder } from "./placeholder";
import { Item, Room, Slot } from "./types";

const SLOT_SIZE = 12;

const fakeBottomBorder = {
  content: "''",
  display: "block",
  borderBottom: "primary",
  width: "100%",
  position: "absolute",
  bottom: "-3px",
  left: 0,
};

const fakeTopBorder = {
  ...fakeBottomBorder,
  borderBottom: "none",
  borderTop: "primary",
  bottom: "auto",
  top: "-3px",
};

const formatHour = (value: string) => {
  const [hour, minutes] = value.split(":");

  return [hour, minutes].join(".");
};
const getRowStartForSlot = ({
  offset,
  index,
}: {
  offset: number;
  index: number;
}) => SLOT_SIZE * index + offset;

const getRowEndForSlot = ({
  offset,
  index,
}: {
  offset: number;
  index: number;
}) => SLOT_SIZE * (index + 1) + offset;

const convertHoursToMinutes = (value: string) => {
  const [hour, minutes] = value.split(":").map(x => parseInt(x, 10));

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

  let endingSlotIndex = slots.findIndex(
    s => convertHoursToMinutes(s.hour) + s.duration >= end,
  );

  let delta = 0;

  if (endingSlotIndex === -1) {
    endingSlotIndex = slots.length - 1;
  }

  const endingSlot = slots[endingSlotIndex];
  const endingSlotEnd =
    convertHoursToMinutes(endingSlot.hour) + endingSlot.duration;
  delta = endingSlotEnd - end;

  const minutesToGridRow = endingSlot.duration / SLOT_SIZE;

  if (delta <= 0) {
    return SLOT_SIZE * (endingSlotIndex + 1) + rowOffset;
  }

  const offset = delta > 0 ? delta / minutesToGridRow : 0;

  return SLOT_SIZE * endingSlotIndex + rowOffset + offset;
};

const getEntryPosition = ({
  item,
  rooms,
  slot,
  slots,
  rowOffset,
}: {
  rowOffset: number;
  item: Item;
  slot: Slot;
  slots: Slot[];
  rooms: Room[];
}) => {
  // find all the indexes for the rooms of this item, then
  // sort them and use the first one for the index of the item
  // this allows us to have items on multiple rooms without having
  // to use complex logic to understand where to position them, as
  // we now assume that the rooms are always consecutive
  const roomIndexes = item.rooms
    .map(room => rooms.findIndex(r => r.id === room.id))
    .sort();

  const index = roomIndexes[0];
  const slotIndex = slots.findIndex(s => s.id === slot.id);

  const rowStart = getRowStartForSlot({
    index: slotIndex,
    offset: rowOffset,
  });

  let rowEnd = getRowEndForSlot({
    index: slotIndex,
    offset: rowOffset,
  });

  if (isTraining(item)) {
    rowEnd = getRowEndForTraining({ item, rowOffset, slot, slots });
  }

  return {
    gridColumnStart: index + 2,
    gridColumnEnd: index + 2 + item.rooms.length,
    gridRowStart: rowStart,
    gridRowEnd: rowEnd,
  };
};

export const Schedule: React.SFC<{
  slots: Slot[];
  rooms: Room[];
  adminMode: boolean;
  addCustomScheduleItem: (slotId: string, rooms: string[]) => void;
  moveItem: (slotId: string, rooms: string[], itemId: string) => void;
  addSubmissionToSchedule: (
    slotId: string,
    rooms: string[],
    submissionId: string,
  ) => void;
}> = ({
  adminMode,
  slots,
  rooms,
  addCustomScheduleItem,
  addSubmissionToSchedule,
  moveItem,
}) => {
  const rowOffset = 6;
  const totalRows = SLOT_SIZE * slots.length + rowOffset;
  const totalColumns = rooms.length;

  const handleDrop = (item: any, slot: Slot, index: number) => {
    if (item.itemId) {
      moveItem(slot.id, [rooms[index].id], item.itemId);
    } else if (item.event.id) {
      addSubmissionToSchedule(slot.id, [rooms[index].id], item.event.id);
    } else {
      const roomIds = item.event.allTracks
        ? rooms.map(room => room.id)
        : [rooms[index].id];

      addCustomScheduleItem(slot.id, roomIds);
    }
  };

  return (
    <Box sx={{ width: "100%", overflowX: "scroll" }}>
      <Grid
        sx={{
          minWidth: "1500px",
          gridTemplateColumns: `80px repeat(${totalColumns}, 1fr)`,
          gridTemplateRows: `repeat(${totalRows - 1}, 10px)`,
          gridGap: "3px",
          py: "3px",
          backgroundColor: "black",
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
              position: "sticky",
              top: 0,
              zIndex: "scheduleHeader",
              "&::after": fakeBottomBorder,
            }}
            style={{
              "--column-start": index + 2,
            }}
          >
            {room.name}
          </Box>
        ))}

        {slots.map((slot, slotIndex) => {
          const rowStart = getRowStartForSlot({
            index: slotIndex,
            offset: rowOffset,
          });

          const rowEnd = getRowEndForSlot({
            index: slotIndex,
            offset: rowOffset,
          });

          return (
            <React.Fragment key={slot.id}>
              <Box
                sx={{
                  gridColumnStart: 1,
                  gridColumnEnd: 1,
                  gridRowStart: "var(--start)",
                  gridRowEnd: "var(--end)",
                  backgroundColor: "white",
                  p: 2,
                  textAlign: "center",
                  fontWeight: "bold",
                }}
                style={{
                  "--start": rowStart,
                  "--end": rowEnd,
                }}
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

              {slot.items.map(item => (
                <ScheduleEntry
                  key={item.id}
                  item={item}
                  slot={slot}
                  rooms={rooms}
                  adminMode={adminMode}
                  sx={{
                    position: "relative",
                    "&::before": fakeTopBorder,
                    "&::after": fakeBottomBorder,
                    ...getEntryPosition({
                      item,
                      rooms,
                      slot,
                      slots,
                      rowOffset,
                    }),
                  }}
                />
              ))}
            </React.Fragment>
          );
        })}
      </Grid>
    </Box>
  );
};
