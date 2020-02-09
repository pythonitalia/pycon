/** @jsx jsx */
import { Box, Grid } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

import { ScheduleEntry } from "./events";
import { Placeholder } from "./placeholder";
import { Room, Slot } from "./types";

const SLOT_SIZE = 12;

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
                p: 3,
                textAlign: "center",
                fontWeight: "bold",
              }}
              style={{
                "--start": rowStart,
                "--end": rowEnd,
              }}
            >
              <Box>{slot.hour}</Box>
            </Box>

            {rooms.map((room, index) => (
              <React.Fragment key={`${room.id}-${slot.id}`}>
                <Placeholder
                  columnStart={index + 2}
                  rowStart={rowStart}
                  rowEnd={rowEnd}
                  duration={slot.duration}
                  roomType={room.type}
                  onDrop={(item: any) => handleDrop(item, slot, index)}
                />

                {slot.items[index] && (
                  <ScheduleEntry
                    item={slot.items[index]}
                    slot={slot}
                    rowStart={rowStart}
                    rowEnd={rowEnd}
                    rooms={rooms}
                  />
                )}
              </React.Fragment>
            ))}
          </React.Fragment>
        );
      })}
    </Grid>
  );
};
