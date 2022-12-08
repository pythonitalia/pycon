import clsx from "clsx";
import React from "react";

type Props = {
  size: "medium" | "large" | "big";
};

export const Spacer = ({ size }: Props) => (
  <span
    className={clsx("block", {
      "h-4": size === "medium",
      "h-10": size === "large",
      "h-20": size === "big",
    })}
  />
);
