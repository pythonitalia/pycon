/** @jsx jsx */
import { Box } from "@theme-ui/components";
import React from "react";
import { useDrag } from "react-dnd";
import { jsx } from "theme-ui";

import { Item, ItemTypes, Room, Slot } from "./types";

const BaseDraggable: React.SFC<{ type: string; metadata?: any }> = ({
  type,
  children,
  metadata,
  ...props
}) => {
  const [_, drag] = useDrag({
    item: {
      type,
      ...metadata,
    },
    collect: monitor => ({
      isDragging: !!monitor.isDragging(),
    }),
  });

  return (
    <Box
      ref={drag}
      sx={{
        cursor: "move",
      }}
      {...props}
    >
      {children}
    </Box>
  );
};

export const BaseEvent: React.SFC<{ type: string; metadata: any }> = ({
  type,
  children,
  metadata,
  ...props
}) => (
  <BaseDraggable
    type={type}
    metadata={metadata}
    sx={{
      display: "inline-block",
      border: "primary",
      p: 3,
      mb: "-3px",
      mr: 3,
    }}
    {...props}
  >
    {children}
  </BaseDraggable>
);

export const Submission = ({
  duration,
  title,
  id,
  ...props
}: {
  id: string;
  title: string;
  duration: number;
}) => {
  const type = `TALK_${duration}`;

  return (
    <BaseEvent type={type} metadata={{ event: { id } }} {...props}>
      {title} {duration}
    </BaseEvent>
  );
};

export const AllTracksEvent = ({ ...props }) => (
  <BaseEvent
    type={ItemTypes.ALL_TRACKS_EVENT}
    metadata={{ event: { allTracks: true } }}
    {...props}
  >
    All track event
  </BaseEvent>
);

export const CustomEvent = ({ ...props }) => (
  <BaseEvent
    type={ItemTypes.CUSTOM}
    metadata={{ event: { title: "Custom" } }}
    {...props}
  >
    Custom event
  </BaseEvent>
);

export const ScheduleEntry: React.SFC<{
  item: Item;
  slot: Slot;
  rowStart: number;
  rowEnd: number;
  rooms: Room[];
}> = ({ item, slot, rowStart, rowEnd, rooms }) => {
  // find all the indexes for the rooms of this item, then
  // sort them and use the first one for the index of the item
  // this allows us to have items on multiple rooms without having
  // to use complex logic to understand where to position them, as
  // we now assume that the rooms are always consecutive
  const roomIndexes = item.rooms
    .map(room => rooms.findIndex(r => r.id === room.id))
    .sort();

  const index = roomIndexes[0];

  const type = `TALK_${slot.duration}`;

  return (
    <BaseDraggable
      type={type}
      sx={{
        gridColumnStart: index + 2,
        gridColumnEnd: index + 2 + item.rooms.length,
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        backgroundColor: "violet",
        position: "relative",
        zIndex: 10,
        p: 3,
      }}
      metadata={{ itemId: item.id }}
    >
      {item.title}
    </BaseDraggable>
  );
};
