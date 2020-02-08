/** @jsx jsx */
import { Box, Grid } from "@theme-ui/components";
import React, { useState } from "react";
import { jsx } from "theme-ui";

import { Placeholder } from "./placeholder";
import { Item as ItemType, Room, ScheduleItem, Slot } from "./types";

const Item: React.SFC<{
  item: ItemType;
  slot: Slot;
  rowOffset: number;
  rooms: Room[];
}> = ({ item, slot, rowOffset, rooms }) => {
  // find all the indexes for the rooms of this item, then
  // sort them and use the first one for the index of the item
  // this allows us to have items on multiple rooms without having
  // to use complex logic to understand where to position them, as
  // we now assume that the rooms are always consecutive
  const roomIndexes = item.rooms
    .map(room => rooms.findIndex(r => r.id === room.id))
    .sort();

  const index = roomIndexes[0];

  return (
    <Box
      sx={{
        gridColumnStart: index + 2,
        gridColumnEnd: index + 2 + item.rooms.length,
        gridRowStart: slot.offset / 5 + rowOffset,
        gridRowEnd: (slot.offset + slot.size) / 5 + rowOffset,
        backgroundColor: "violet",
        position: "relative",
        zIndex: 10,
        p: 3,
      }}
    >
      {item.title}
    </Box>
  );
};

export const Schedule: React.SFC<{
  slots: Slot[];
  rooms: Room[];
  addCustomScheduleItem: (slotId: string, rooms: string[]) => void;
  addSubmissionToSchedule: (
    slotId: string,
    rooms: string[],
    submissionId: string,
  ) => void;
}> = ({ slots, rooms, addCustomScheduleItem, addSubmissionToSchedule }) => {
  const rowOffset = 6;
  const totalRows =
    slots.reduce((total, slot) => slot.size + total, 0) / 5 + rowOffset;
  const totalColumns = rooms.length;

  const handleDrop = (item: any, slot: Slot, index: number) => {
    // TODO: move and full conf events

    if (item.event.id) {
      addSubmissionToSchedule(slot.id, [rooms[index].id], item.event.id);
    } else {
      addCustomScheduleItem(slot.id, [rooms[index].id]);
    }
  };

  return (
    <Grid
      sx={{
        gridTemplateColumns: `100px repeat(${totalColumns}, 1fr)`,
        gridTemplateRows: `repeat(${totalRows - 1}, 10px)`,
        gridGap: "4px",
        py: "4px",
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
            gridColumnStart: index + 2,
            gridRowStart: 1,
            gridRowEnd: rowOffset,
            backgroundColor: "white",
            py: 2,
            px: 3,
            fontWeight: "bold",
          }}
        >
          {room.name}
        </Box>
      ))}

      {slots.map(slot => (
        <React.Fragment key={slot.hour.toString()}>
          <Box
            sx={{
              gridColumnStart: 1,
              gridColumnEnd: 1,
              gridRowStart: "var(--start)",
              gridRowEnd: "var(--end)",
              backgroundColor: "white",
              p: 3,
              textAlign: "center",
              fontWeight: "bold",
            }}
            style={{
              "--start": slot.offset / 5 + rowOffset,
              "--end": (slot.offset + slot.size) / 5 + rowOffset,
            }}
          >
            <Box>{slot.hour}</Box>
          </Box>

          {rooms.map((_, index) => (
            <React.Fragment key={`${index}-${slot.duration}-${slot.offset}`}>
              <Placeholder
                columnStart={index + 2}
                rowStart={slot.offset / 5 + rowOffset}
                rowEnd={(slot.offset + slot.size) / 5 + rowOffset}
                duration={slot.duration}
                onDrop={(item: any) => handleDrop(item, slot, index)}
              />

              {slot.items[index] && (
                <Item
                  item={slot.items[index]}
                  slot={slot}
                  rowOffset={rowOffset}
                  rooms={rooms}
                />
              )}
            </React.Fragment>
          ))}
        </React.Fragment>
      ))}
    </Grid>
  );
};
