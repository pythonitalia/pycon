/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Button, Flex, Grid, Heading } from "@theme-ui/components";
import moment from "moment";
import React, { useEffect, useLayoutEffect, useState } from "react";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import Backend from "react-dnd-html5-backend";
import { jsx } from "theme-ui";

import { useConference } from "../../context/conference";
import {
  ScheduleQuery,
  ScheduleQueryVariables,
} from "../../generated/graphql-backend";
import SCHEDULE_QUERY from "./schedule.graphql";

const ItemTypes = {
  TALK_30: "talk_30",
  TALK_45: "talk_45",
  TALK_60: "talk_60",
};

const BaseEvent: React.SFC<{ type: string; metadata: any }> = ({
  type,
  children,
  metadata,
}) => {
  const [_, drag] = useDrag({
    item: {
      type,
      event: metadata,
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
      {children}
    </Box>
  );
};

const Talk = ({ duration }: { duration: 30 | 45 | 60 }) => {
  const type = `TALK_${duration}` as keyof typeof ItemTypes;

  return (
    <BaseEvent type={ItemTypes[type]} metadata={{ title: "example" }}>
      Talk {duration}
    </BaseEvent>
  );
};

const AllTracksEvent = () => (
  <BaseEvent
    type="ALL_TRACKS_EVENT"
    metadata={{ title: "Lunch", allTracks: true }}
  >
    Lunch
  </BaseEvent>
);

const Placeholder: React.SFC<{
  columnStart: number;
  rowStart: number;
  rowEnd: number;
  duration: number;
  onDrop: (item: any) => void;
}> = ({ columnStart, rowStart, rowEnd, duration, onDrop }) => {
  const type = `TALK_${duration}` as keyof typeof ItemTypes;

  const [{ isOver, canDrop }, drop] = useDrop({
    accept: [ItemTypes[type], "ALL_TRACKS_EVENT"],
    drop: onDrop,
    collect: mon => ({
      isOver: !!mon.isOver(),
      canDrop: !!mon.canDrop(),
    }),
  });

  const backgroundColor = isOver ? "green" : canDrop ? "orange" : "white";

  return (
    <Box
      ref={drop}
      sx={{
        gridColumnStart: columnStart,
        gridColumnEnd: columnStart + 1,
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        backgroundColor,
        p: 3,
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

type ScheduleItem = {
  title: string;
  trackSpan?: number;
  allTracks?: boolean;
};

type Room = {
  name: string;
};

const formatDay = (day: string) => {
  const d = new Date(day);

  const formatter = new Intl.DateTimeFormat("default", {
    weekday: "long",
    day: "numeric",
    // TODO: use conference timezone
    timeZone: "Europe/Rome",
  });

  return formatter.format(d);
};

const Schedule: React.SFC<{ slots: Slot[]; rooms: Room[] }> = ({
  slots,
  rooms,
}) => {
  const rowOffset = 6;
  const totalRows =
    slots.reduce((total, slot) => slot.size + total, 0) / 5 + rowOffset;
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

      {slots.map(slot => {
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
              <Box>{slot.hour.format("hh:mm")}</Box>
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

const DaySelector: React.SFC<{
  setCurrentDay: (day: string) => void;
  currentDay: string | null;
  days: { day: string }[];
}> = ({ currentDay, days, setCurrentDay }) => (
  <Box as="ul" sx={{ ml: "auto" }}>
    {days.map(day => (
      <Box
        key={day.day}
        as="li"
        sx={{
          listStyle: "none",
          display: "inline-block",
        }}
      >
        <Button
          onClick={() => setCurrentDay(day.day)}
          sx={{
            backgroundColor: currentDay === day.day ? "violet" : "white",
            mr: "-3px",
            "&:hover": {
              backgroundColor: "lightViolet",
            },
          }}
        >
          {formatDay(day.day)}
        </Button>
      </Box>
    ))}
  </Box>
);

export const ScheduleScreen: React.SFC<RouteComponentProps> = () => {
  const { code } = useConference();

  const [slots, addSlot] = useSlots();
  // TODO: redirect to today or first day when we add per day routes
  const [currentDay, setCurrentDay] = useState<string | null>(null);

  const { loading, data, error } = useQuery<
    ScheduleQuery,
    ScheduleQueryVariables
  >(SCHEDULE_QUERY, {
    variables: {
      code,
    },
  });

  useLayoutEffect(() => {
    if (!currentDay && data?.conference) {
      setCurrentDay(data.conference.days[0].day);
    }
  }, [data]);

  if (loading) {
    return <Box>Loading</Box>;
  }

  if (error) {
    throw error;
  }

  const { rooms, days } = data?.conference!;

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

              <AllTracksEvent />
            </React.Fragment>
          ))}
        </Box>
      </Box>

      <Box sx={{ flex: 1 }}>
        <Box sx={{ backgroundColor: "orange", borderTop: "primary" }}>
          <Flex sx={{ py: 4, px: 3, maxWidth: "largeContainer", mx: "auto" }}>
            <Heading sx={{ fontSize: 6 }}>Schedule</Heading>

            <DaySelector
              days={days}
              currentDay={currentDay}
              setCurrentDay={setCurrentDay}
            />
          </Flex>
        </Box>

        <Schedule slots={slots} rooms={rooms} />

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
