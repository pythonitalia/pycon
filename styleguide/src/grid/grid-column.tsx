import React from "react";
import clsx from "clsx";

type Props = {
  children: React.ReactNode;
  colSpan?: number;
  mdColSpan?: number;
  rowSpan?: number;
  mdRowSpan?: number;
  className?: string;
};

export const GridColumn = ({
  children,
  colSpan,
  mdColSpan,
  rowSpan,
  mdRowSpan,
  className,
}: Props) => {
  return (
    <div
      className={clsx(
        {
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

          "md:col-span-1": mdColSpan === 1,
          "md:col-span-2": mdColSpan === 2,
          "md:col-span-3": mdColSpan === 3,
          "md:col-span-4": mdColSpan === 4,
          "md:col-span-5": mdColSpan === 5,
          "md:col-span-6": mdColSpan === 6,
          "md:col-span-7": mdColSpan === 7,
          "md:col-span-8": mdColSpan === 8,
          "md:col-span-9": mdColSpan === 9,
          "md:col-span-10": mdColSpan === 10,
          "md:col-span-11": mdColSpan === 11,
          "md:col-span-12": mdColSpan === 12,

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

          "md:row-span-1": mdRowSpan === 1,
          "md:row-span-2": mdRowSpan === 2,
          "md:row-span-3": mdRowSpan === 3,
          "md:row-span-4": mdRowSpan === 4,
          "md:row-span-5": mdRowSpan === 5,
          "md:row-span-6": mdRowSpan === 6,
          "md:row-span-7": mdRowSpan === 7,
          "md:row-span-8": mdRowSpan === 8,
          "md:row-span-9": mdRowSpan === 9,
          "md:row-span-10": mdRowSpan === 10,
          "md:row-span-11": mdRowSpan === 11,
          "md:row-span-12": mdRowSpan === 12,
        },
        className
      )}
    >
      {children}
    </div>
  );
};
