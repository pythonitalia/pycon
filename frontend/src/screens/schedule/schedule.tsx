/** @jsx jsx */
import { Box, Grid } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

import { ScheduleEntry } from "./events";
import { Placeholder } from "./placeholder";
import { Room, Slot } from "./types";

export const Schedule: React.SFC<{
  slots: Slot[];
  rooms: Room[];
  addCustomScheduleItem: (slotId: string, rooms: string[]) => void;
  moveItem: (slotId: string, rooms: string[], itemId: string) => void;
  addSubmissionToSchedule: (
    slotId: string,
    rooms: string[],
    submissionId: string,
  ) => void;
}> = ({
  slots,
  rooms,
  addCustomScheduleItem,
  addSubmissionToSchedule,
  moveItem,
}) => {
  const rowOffset = 6;
  const totalRows =
    slots.reduce((total, slot) => slot.size + total, 0) / 5 + rowOffset;
  const totalColumns = rooms.length;

  const handleDrop = (item: any, slot: Slot, index: number) => {
    // TODO: full conf events
    if (item.itemId) {
      moveItem(slot.id, [rooms[index].id], item.itemId);
    } else if (item.event.id) {
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
                <ScheduleEntry
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
