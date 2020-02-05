/** @jsx jsx */
import { Box } from "@theme-ui/components";
import React from "react";
import { useDrag } from "react-dnd";
import { jsx } from "theme-ui";

import { ItemTypes } from "./types";

export const BaseEvent: React.SFC<{ type: string; metadata: any }> = ({
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

export const Talk = ({ duration }: { duration: 30 | 45 | 60 }) => {
  const type = `TALK_${duration}` as keyof typeof ItemTypes;

  return (
    <BaseEvent type={ItemTypes[type]} metadata={{ title: "example" }}>
      Talk {duration}
    </BaseEvent>
  );
};

export const AllTracksEvent = () => (
  <BaseEvent
    type={ItemTypes.ALL_TRACKS_EVENT}
    metadata={{ title: "Lunch", allTracks: true }}
  >
    Lunch
  </BaseEvent>
);
