import clsx from "clsx";
import React from "react";

type Props = {
  cols: number;
  children: React.ReactNode;
  alignItems?: "start" | "center" | "end";
};

export const Grid = ({ cols, children, alignItems }: Props) => {
  return (
    <div
      className={clsx("grid gap-6", {
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

        "lg:items-start": alignItems === "start",
        "lg:items-center": alignItems === "center",
        "lg:items-end": alignItems === "end",
      })}
    >
      {children}
    </div>
  );
};
