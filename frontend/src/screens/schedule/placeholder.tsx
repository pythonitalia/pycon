/** @jsx jsx */
import { Box } from "@theme-ui/components";
import React from "react";
import { useDrop } from "react-dnd";
import { jsx } from "theme-ui";

import { ItemTypes } from "./types";

export const Placeholder: React.SFC<{
  columnStart: number;
  rowStart: number;
  rowEnd: number;
  duration: number;
  roomType: string;
  onDrop: (item: any) => void;
}> = ({ columnStart, rowStart, rowEnd, duration, roomType, onDrop }) => {
  const accept = [`TALK_${duration}`, ItemTypes.CUSTOM];

  if (columnStart === 2) {
    accept.push(ItemTypes.ALL_TRACKS_EVENT);
  }

  if (roomType === "training") {
    accept.push(ItemTypes.TRAINING);
  }

  const [{ isOver, canDrop }, drop] = useDrop({
    accept,
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
