import clsx from "clsx";
import React from "react";

type Props = {
  mobileOnly?: boolean;
  hidden?: boolean;
  escapeContainer?: boolean | "mobile";
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

      "w-screen -ml-4": escapeContainer === true,
      "w-screen -ml-4 md:w-auto md:ml-0": escapeContainer === "mobile",
      "w-full": orientation === "horizontal" && escapeContainer === false,

      "h-separator": orientation === "horizontal",
      "w-separator": orientation === "vertical",
    })}
  />
);
