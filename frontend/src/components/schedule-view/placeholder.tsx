import React from "react";

export const Placeholder = ({
  columnStart,
  rowStart,
  rowEnd,
}: {
  columnStart: number;
  rowStart: number;
  rowEnd: number;
  duration: number;
  roomType: string;
}) => {
  return (
    <div
      className="hidden md:block p-2"
      style={{
        gridColumnStart: columnStart,
        gridColumnEnd: columnStart + 1,
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
        backgroundColor: "#FAF5F3",
      }}
    ></div>
  );
};
