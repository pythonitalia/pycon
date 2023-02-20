import clsx from "clsx";
import React, { ReactNode } from "react";

type Props = {
  children: ReactNode;
  alignItems?: "start" | "center" | "end";
  justifyContent?: "start" | "center" | "end" | "spaceBetween" | "spaceAround";
  wrap?: "wrap" | "wrapMobileOnly" | "nowrap" | "wrapReverse";
  gap?: "none" | "small" | "medium";
  reverse?: boolean;
  fullWidth?: boolean;
};

export const HorizontalStack = ({
  children,
  gap = "none",
  alignItems,
  justifyContent,
  wrap,
  reverse = false,
  fullWidth = false,
}: Props) => (
  <div
    className={clsx("flex", {
      "flex-row": !reverse,
      "flex-row-reverse": reverse,

      "w-full": fullWidth,

      "items-start": alignItems === "start",
      "items-center": alignItems === "center",
      "items-end": alignItems === "end",

      "justify-start": justifyContent === "start",
      "justify-center": justifyContent === "center",
      "justify-end": justifyContent === "end",
      "justify-between": justifyContent === "spaceBetween",
      "justify-around": justifyContent === "spaceAround",

      "flex-wrap": wrap === "wrap",
      "flex-wrap lg:flex-nowrap": wrap === "wrapMobileOnly",
      "flex-nowrap": wrap === "nowrap",
      "flex-wrap-reverse": wrap === "wrapReverse",

      "gap-0": gap === "none",
      "gap-2 lg:gap-4": gap === "small",
      "gap-2 lg:gap-6": gap === "medium",
    })}
  >
    {children}
  </div>
);
