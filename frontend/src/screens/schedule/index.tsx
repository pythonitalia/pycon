/** @jsx jsx */
import { RouteComponentProps } from "@reach/router";
import { Box, Button, Flex, Grid } from "@theme-ui/components";
import moment from "moment";
import React, { useState } from "react";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import Backend from "react-dnd-html5-backend";
import { jsx } from "theme-ui";

import { useConference } from "../../context/conference";

const ItemTypes = {
  TALK_30: "talk_30",
  TALK_45: "talk_45",
  TALK_60: "talk_60",
};

const Talk = ({ duration }: { duration: 30 | 45 | 60 }) => {
  const type = `TALK_${duration}` as keyof typeof ItemTypes;

  const [{ isDragging }, drag] = useDrag({
    item: {
      type: ItemTypes[type],
      talk: {
        title: "Talk title",
      },
    },
    collect: monitor => ({
      isDragging: !!monitor.isDragging(),
    }),
  });

  return (
    <Box
      ref={drag}
      sx={{
        display: "inline-block",
        border: "primary",
        p: 3,
        mb: "-3px",
        mr: 3,
        cursor: "move",
      }}
    >
      Talk {duration}
    </Box>
  );
};

const Placeholder: React.SFC<{
  columnStart: number;
  rowStart: number;
  rowEnd: number;
  duration: number;
  onDrop: (item: any) => void;
}> = ({ columnStart, rowStart, rowEnd, duration, onDrop }) => {
  const type = `TALK_${duration}` as keyof typeof ItemTypes;

  const [{ isOver, canDrop }, drop] = useDrop({
    accept: ItemTypes[type],
    drop: onDrop,
    collect: mon => ({
      isOver: !!mon.isOver(),
      canDrop: !!mon.canDrop(),
    }),
  });

  const backgroundColor = isOver ? "green" : canDrop ? "orange" : "";

  return (
    <Box
      ref={drop}
      sx={{
        gridColumnStart: columnStart,
        gridColumnEnd: columnStart + 1,
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        borderBottom: "primary",
        borderRight: "primary",
        backgroundColor,
      }}
    >
      Placeholder {duration}
    </Box>
  );
};

type Slot = {
  duration: number;
  hour: moment.Moment;
  size: number;
  offset: number;
};

const useSlots = (): [Slot[], (duration: number) => void] => {
  const [slots, setSlots] = useState<Slot[]>([]);

  const addSlot = (duration: number) => {
    const lastSlot = slots.length > 0 ? slots[slots.length - 1] : null;

    const hour = lastSlot
      ? lastSlot.hour.clone().add(duration, "minutes")
      : moment()
          .hour(8)
          .minute(45);
    const offset = lastSlot ? lastSlot.offset + lastSlot.size : 0;

    setSlots([
      ...slots,
      {
        duration,
        hour,
        // we use this instead of duration to calculate the dimension on the grid
        size: 45,
        offset,
      },
    ]);
  };

  return [slots, addSlot];
};

const Schedule: React.SFC<{ slots: Slot[] }> = ({ slots }) => {
  const rowOffset = 5;
  const totalRows =
    slots.reduce((total, slot) => slot.size + total, 0) / 5 + rowOffset;
  const totalColumns = 7;

  // "slotHour": { "track" : {}}

  const [talks, setTalks] = useState<{
    [hour: number]: { [track: number]: number };
  }>({});

  const handleDrop = (item: any, slot: Slot, index: number) => {
    const slotHour = slot.hour.valueOf();

    setTalks({
      ...talks,
      [slotHour]: {
        ...(talks[slotHour] || {}),
        [index]: item.talk,
      },
    });
  };

  console.log(talks);

  return (
    <Grid
      sx={{
        gridTemplateColumns: `100px repeat(${totalColumns}, 1fr)`,
        gridTemplateRows: `repeat(${totalRows}, 10px)`,
        gridGap: 0,
      }}
    >
      <Box
        sx={{ borderBottom: "primary", gridRowStart: 1, gridRowEnd: rowOffset }}
      />
      {new Array(totalColumns).fill(null).map((_, index) => (
        <Box
          key={index}
          sx={{
            gridColumnStart: index + 2,
            gridRowStart: 1,
            gridRowEnd: rowOffset,
            borderBottom: "primary",
          }}
        >
          Track {index}
        </Box>
      ))}

      {slots.map(slot => {
        const slotTalks = talks[slot.hour.valueOf()] || {};

        return (
          <React.Fragment key={slot.hour.toString()}>
            <Box
              sx={{
                gridColumnStart: 1,
                gridColumnEnd: 1,
                gridRowStart: "var(--start)",
                gridRowEnd: "var(--end)",
                borderBottom: "primary",
                borderRight: "primary",
              }}
              style={{
                "--start": slot.offset / 5 + rowOffset,
                "--end": (slot.offset + slot.size) / 5 + rowOffset,
              }}
            >
              <Box>{slot.hour.format("hh:mm")}</Box>
            </Box>

            {new Array(totalColumns).fill(null).map((_, index) => (
              <React.Fragment key={index}>
                <Placeholder
                  columnStart={index + 2}
                  rowStart={slot.offset / 5 + rowOffset}
                  rowEnd={(slot.offset + slot.size) / 5 + rowOffset}
                  duration={slot.duration}
                  onDrop={(item: any) => handleDrop(item, slot, index)}
                />

                {slotTalks[index] && (
                  <Box
                    sx={{
                      gridColumnStart: index + 2,
                      gridColumnEnd: index + 2 + 1,
                      gridRowStart: slot.offset / 5 + rowOffset,
                      gridRowEnd: (slot.offset + slot.size) / 5 + rowOffset,
                      backgroundColor: "violet",
                    }}
                  >
                    {slotTalks[index].title}
                  </Box>
                )}
              </React.Fragment>
            ))}
          </React.Fragment>
        );
      })}
    </Grid>
  );
};

export const ScheduleScreen: React.SFC<RouteComponentProps> = () => {
  const { code } = useConference();

  const [slots, addSlot] = useSlots();

  return (
    <DndProvider backend={Backend}>
      <Box
        sx={{
          position: "fixed",
          bottom: 0,
          left: 0,
          right: 0,
          zIndex: 100,
          padding: 4,
          background: "white",
        }}
      >
        List of talks
        <Box sx={{ overflowY: "scroll", whiteSpace: "nowrap", py: 3 }}>
          {new Array(100).fill(null).map((_, index) => (
            <React.Fragment key={index}>
              <Talk duration={45} />
              <Talk duration={30} />
              <Talk duration={60} />
            </React.Fragment>
          ))}
        </Box>
      </Box>

      <Box sx={{ flex: 1 }}>
        <Schedule slots={slots} />

        <Box mt={4}>
          <Button sx={{ mr: 3 }} onClick={() => addSlot(30)}>
            Add 30 minutes slot
          </Button>
          <Button sx={{ mr: 3 }} onClick={() => addSlot(45)}>
            Add 45 minutes slot
          </Button>
          <Button sx={{ mr: 3 }} onClick={() => addSlot(60)}>
            Add 60 minutes slot
          </Button>
        </Box>
      </Box>
    </DndProvider>
  );
};
