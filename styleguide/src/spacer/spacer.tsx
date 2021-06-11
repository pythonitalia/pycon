import clsx from "clsx";
import React from "react";

type Props = {
  size: "medium";
};

export const Spacer = ({ size }: Props) => (
  <span
    className={clsx("block", {
      "h-4": size === "medium",
    })}
  />
);
