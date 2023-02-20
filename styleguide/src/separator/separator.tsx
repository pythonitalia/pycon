import clsx from "clsx";
import React from "react";

type Props = {
  mobileOnly?: boolean;
  hidden?: boolean;
  escapeContainer?: boolean;
  orientation?: "horizontal" | "vertical";
};

export const Separator = ({
  escapeContainer = false,
  hidden = false,
  mobileOnly = false,
  orientation = "horizontal",
}: Props) => (
  <div
    className={clsx("bg-black", {
      "lg:hidden": mobileOnly,
      hidden,
      "w-screen -ml-4": escapeContainer,
      "w-full": orientation === "horizontal" && !escapeContainer,

      "h-separator": orientation === "horizontal",
      "w-separator": orientation === "vertical",
    })}
  />
);
