import React from "react";
import clsx from "clsx";

type Props = {
  children: React.ReactNode;
  colSpan?: number;
  rowSpan?: number;
};

export const GridColumn = ({ children, colSpan, rowSpan }: Props) => {
  return (
    <div
      className={clsx({
        "lg:col-span-1": colSpan === 1,
        "lg:col-span-2": colSpan === 2,
        "lg:col-span-3": colSpan === 3,
        "lg:col-span-4": colSpan === 4,
        "lg:col-span-5": colSpan === 5,
        "lg:col-span-6": colSpan === 6,
        "lg:col-span-7": colSpan === 7,
        "lg:col-span-8": colSpan === 8,
        "lg:col-span-9": colSpan === 9,
        "lg:col-span-10": colSpan === 10,
        "lg:col-span-11": colSpan === 11,
        "lg:col-span-12": colSpan === 12,

        "lg:row-span-1": rowSpan === 1,
        "lg:row-span-2": rowSpan === 2,
        "lg:row-span-3": rowSpan === 3,
        "lg:row-span-4": rowSpan === 4,
        "lg:row-span-5": rowSpan === 5,
        "lg:row-span-6": rowSpan === 6,
        "lg:row-span-7": rowSpan === 7,
        "lg:row-span-8": rowSpan === 8,
        "lg:row-span-9": rowSpan === 9,
        "lg:row-span-10": rowSpan === 10,
        "lg:row-span-11": rowSpan === 11,
        "lg:row-span-12": rowSpan === 12,
      })}
    >
      {children}
    </div>
  );
};
