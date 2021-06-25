import React from "react";
import { ThemeUIStyleObject } from "theme-ui";

type DIRECTION = "left" | "right";

const getTransform = (direction: DIRECTION) => {
  switch (direction) {
    case "left":
      return "";
    case "right":
      return "rotate(180deg)";
  }
};

type ArrowIconProps = {
  direction?: DIRECTION;
  onClick?: () => void;
  viewBox?: string;
  sx?: ThemeUIStyleObject;
};

export const ArrowIcon = ({ direction = "left", ...props }: ArrowIconProps) => (
  <svg viewBox="0 0 46 53" fill="none" {...props}>
    <g
      style={{ transform: getTransform(direction), transformOrigin: "center" }}
    >
      <path d="M0 26.5L45.75.086v52.828L0 26.5z" fill="#000" />
      <path d="M0 26.5L45.75.086v52.828L0 26.5z" stroke="#000" />
    </g>
  </svg>
);
