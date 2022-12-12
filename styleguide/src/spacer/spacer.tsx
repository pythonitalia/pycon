import clsx from "clsx";
import React from "react";

type Props = {
  size: "medium" | "large" | "xl";
};

export const Spacer = ({ size }: Props) => (
  <span
    className={clsx("block", {
      "h-6": size === "medium",
      "h-12": size === "large",
      "h-12 lg:h-16": size === "xl",
    })}
  />
);
