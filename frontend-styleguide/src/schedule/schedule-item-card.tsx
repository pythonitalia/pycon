import clsx from "clsx";
import React from "react";
import type { ReactNode } from "react";
import { getBackgroundClasses } from "../colors-utils";
import type { Color } from "../types";

type Props = {
  children: ReactNode;
  size: "small" | "large";
  background: Color;
};
export const ScheduleItemCard = ({ children, size, background }: Props) => {
  return (
    <div
      className={clsx(
        "h-full",
        {
          "py-4 px-6": size === "small",
          "py-6 px-6": size === "large",
        },
        getBackgroundClasses(background),
      )}
    >
      {children}
    </div>
  );
};
