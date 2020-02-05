/** @jsx jsx */
import { Box, Grid } from "@theme-ui/components";
import React, { useState } from "react";
import { jsx } from "theme-ui";

import { Placeholder } from "./placeholder";
import { Room, ScheduleItem, Slot } from "./types";

export const Schedule: React.SFC<{
  configuration: Slot[];
  rooms: Room[];
}> = ({ configuration, rooms }) => {
  const rowOffset = 6;
  const totalRows =
    configuration.reduce((total, slot) => slot.size + total, 0) / 5 + rowOffset;
  const totalColumns = rooms.length;

  const [scheduleItems, setScheduleItems] = useState<{
    [hour: number]: { [track: number]: ScheduleItem };
  }>({});

  const handleDrop = (item: any, slot: Slot, index: number) => {
    const slotHour = slot.hour.valueOf();

    setScheduleItems({
      ...scheduleItems,
      [slotHour]: {
        ...(scheduleItems[slotHour] || {}),
        [index]: item.event,
      },
    });
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

      {configuration.map(slot => {
        const slotScheduleItems = scheduleItems[slot.hour.valueOf()] || {};

        return (
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

            {rooms.map((_, index) => {
              const scheduleItem = slotScheduleItems[index];

              return (
                <React.Fragment key={index}>
                  <Placeholder
                    columnStart={index + 2}
                    rowStart={slot.offset / 5 + rowOffset}
                    rowEnd={(slot.offset + slot.size) / 5 + rowOffset}
                    duration={slot.duration}
                    onDrop={(item: any) => handleDrop(item, slot, index)}
                  />

                  {scheduleItem && (
                    <Box
                      sx={{
                        gridColumnStart: index + 2,
                        gridColumnEnd:
                          index +
                          2 +
                          (scheduleItem.allTracks
                            ? rooms.length
                            : scheduleItem.trackSpan || 1),
                        gridRowStart: slot.offset / 5 + rowOffset,
                        gridRowEnd: (slot.offset + slot.size) / 5 + rowOffset,
                        backgroundColor: "violet",
                        position: "relative",
                        zIndex: 10,
                        p: 3,
                      }}
                    >
                      {scheduleItem.title}
                    </Box>
                  )}
                </React.Fragment>
              );
            })}
          </React.Fragment>
        );
      })}
    </Grid>
  );
};
