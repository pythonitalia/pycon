import clsx from "clsx";
import React from "react";

export type GridCols = number;

type Props = {
  cols: GridCols;
  mdCols?: GridCols;
  children: React.ReactNode;
  alignItems?: "start" | "center" | "end";
  gap?: "none" | "small" | "medium";
  smCols?: GridCols;
  divide?: boolean;
  equalHeight?: boolean;
  fullWidth?: boolean;
  className?: string;
};

export const Grid = ({
  cols,
  mdCols,
  smCols,
  children,
  alignItems,
  gap = "medium",
  divide = false,
  equalHeight = false,
  fullWidth = false,
  className,
}: Props) => {
  return (
    <div
      className={clsx(
        "grid",
        {
          "lg:grid-cols-1": cols === 1,
          "lg:grid-cols-2": cols === 2,
          "lg:grid-cols-3": cols === 3,
          "lg:grid-cols-4": cols === 4,
          "lg:grid-cols-5": cols === 5,
          "lg:grid-cols-6": cols === 6,
          "lg:grid-cols-7": cols === 7,
          "lg:grid-cols-8": cols === 8,
          "lg:grid-cols-9": cols === 9,
          "lg:grid-cols-10": cols === 10,
          "lg:grid-cols-11": cols === 11,
          "lg:grid-cols-12": cols === 12,

          "md:grid-cols-1": mdCols === 1,
          "md:grid-cols-2": mdCols === 2,
          "md:grid-cols-3": mdCols === 3,
          "md:grid-cols-4": mdCols === 4,
          "md:grid-cols-5": mdCols === 5,
          "md:grid-cols-6": mdCols === 6,
          "md:grid-cols-7": mdCols === 7,
          "md:grid-cols-8": mdCols === 8,
          "md:grid-cols-9": mdCols === 9,
          "md:grid-cols-10": mdCols === 10,
          "md:grid-cols-11": mdCols === 11,
          "md:grid-cols-12": mdCols === 12,

          "grid-cols-1": smCols === 1,
          "grid-cols-2": smCols === 2,
          "grid-cols-3": smCols === 3,
          "grid-cols-4": smCols === 4,
          "grid-cols-5": smCols === 5,
          "grid-cols-6": smCols === 6,
          "grid-cols-7": smCols === 7,
          "grid-cols-8": smCols === 8,
          "grid-cols-9": smCols === 9,
          "grid-cols-10": smCols === 10,
          "grid-cols-11": smCols === 11,
          "grid-cols-12": smCols === 12,

          "grid-cols-[100%]": !smCols,

          "lg:items-start": alignItems === "start",
          "lg:items-center": alignItems === "center",
          "lg:items-end": alignItems === "end",

          "gap-2 lg:gap-4": gap === "small",
          "gap-2 lg:gap-6": gap === "medium",

          "md:auto-rows-fr": equalHeight,

          // weird bug in tailwind where divide-y-0 doesn't work
          "divide-y lg:divide-y-[0px] lg:divide-x": divide,

          "w-full": fullWidth,
        },
        className
      )}
    >
      {children}
    </div>
  );
};
