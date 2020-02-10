/** @jsx jsx */
import { Box } from "@theme-ui/components";
import React from "react";
import { useDrag } from "react-dnd";
import { jsx } from "theme-ui";

import { getColorForSubmission } from "./get-color-for-submission";
import {
  Item,
  ItemTypes,
  Room,
  Slot,
  Submission as SubmissionType,
} from "./types";

const COLOR_MAP = {
  custom: "cinderella",
};

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
  submission,
  ...props
}: {
  submission: SubmissionType;
}) => {
  const itemType =
    submission.type?.name.toLocaleLowerCase() === "tutorial"
      ? ItemTypes.TRAINING
      : `TALK_${submission.duration!.duration}`;

  return (
    <BaseEvent
      type={itemType}
      metadata={{ event: { id: submission.id } }}
      sx={{ backgroundColor: getColorForSubmission(submission) }}
      {...props}
    >
      {submission.title} {submission.duration!.duration}
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
  rooms: Room[];
}> = ({ item, slot, rooms, ...props }) => {
  // TODO: training type
  const type = `TALK_${slot.duration}`;

  const backgroundColor =
    item.type === "submission" && item.submission
      ? getColorForSubmission(item.submission)
      : COLOR_MAP.custom;

  return (
    <BaseDraggable
      type={type}
      sx={{
        backgroundColor,
        position: "relative",
        zIndex: 10,
        p: 3,
      }}
      {...props}
      metadata={{ itemId: item.id }}
    >
      {item.title}
    </BaseDraggable>
  );
};
