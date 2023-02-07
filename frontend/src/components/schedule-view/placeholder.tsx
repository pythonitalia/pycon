import React from "react";

import { ItemTypes } from "./types";
import { useDropOrDummy } from "./use-drop-or-dummy";

export const Placeholder = ({
  adminMode,
  columnStart,
  rowStart,
  rowEnd,
  duration,
  roomType,
  onDrop,
}: {
  adminMode: boolean;
  columnStart: number;
  rowStart: number;
  rowEnd: number;
  duration: number;
  roomType: string;
  onDrop: (item: any) => void;
}) => {
  const accept = [`TALK_${duration}`, ItemTypes.TALK, ItemTypes.CUSTOM];

  if (columnStart === 2) {
    accept.push(ItemTypes.ALL_TRACKS_EVENT);
    accept.push(ItemTypes.KEYNOTE);
  }

  if (roomType === "training") {
    accept.push(ItemTypes.TRAINING);
  }

  const [{ isOver, canDrop }, drop] = useDropOrDummy({
    adminMode,
    accept,
    drop: onDrop,
    collect: (mon) => ({
      isOver: !!mon.isOver(),
      canDrop: !!mon.canDrop(),
    }),
  });

  const backgroundColor = isOver ? "green" : canDrop ? "orange" : "#FAF5F3";

  return (
    <div
      ref={adminMode ? drop : null}
      className="hidden md:block p-2"
      style={{
        gridColumnStart: columnStart,
        gridColumnEnd: columnStart + 1,
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        backgroundColor,
      }}
    >
      {adminMode && `Placeholder ${duration}`}
    </div>
  );
};
