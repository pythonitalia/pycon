import React from "react";
import clsx from "clsx";

type Props = {
  children?: React.ReactNode;
  colSpan?: number;
  mdColSpan?: number;

  colStart?: number;
  mdColStart?: number;

  colEnd?: number;
  mdColEnd?: number;

  rowSpan?: number;
  mdRowSpan?: number;

  rowStart?: number;
  mdRowStart?: number;

  rowEnd?: number;
  mdRowEnd?: number;

  className?: string;
};

export const GridColumn = ({
  children,

  colSpan,
  mdColSpan,

  colStart,
  mdColStart,

  colEnd,
  mdColEnd,

  rowSpan,
  mdRowSpan,

  rowStart,
  mdRowStart,

  rowEnd,
  mdRowEnd,

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

          "lg:col-start-1": colStart === 1,
          "lg:col-start-2": colStart === 2,
          "lg:col-start-3": colStart === 3,
          "lg:col-start-4": colStart === 4,
          "lg:col-start-5": colStart === 5,
          "lg:col-start-6": colStart === 6,
          "lg:col-start-7": colStart === 7,
          "lg:col-start-8": colStart === 8,
          "lg:col-start-9": colStart === 9,
          "lg:col-start-10": colStart === 10,
          "lg:col-start-11": colStart === 11,
          "lg:col-start-12": colStart === 12,

          "md:col-start-1": mdColStart === 1,
          "md:col-start-2": mdColStart === 2,
          "md:col-start-3": mdColStart === 3,
          "md:col-start-4": mdColStart === 4,
          "md:col-start-5": mdColStart === 5,
          "md:col-start-6": mdColStart === 6,
          "md:col-start-7": mdColStart === 7,
          "md:col-start-8": mdColStart === 8,
          "md:col-start-9": mdColStart === 9,
          "md:col-start-10": mdColStart === 10,
          "md:col-start-11": mdColStart === 11,
          "md:col-start-12": mdColStart === 12,

          "lg:col-end-1": colEnd === 1,
          "lg:col-end-2": colEnd === 2,
          "lg:col-end-3": colEnd === 3,
          "lg:col-end-4": colEnd === 4,
          "lg:col-end-5": colEnd === 5,
          "lg:col-end-6": colEnd === 6,
          "lg:col-end-7": colEnd === 7,
          "lg:col-end-8": colEnd === 8,
          "lg:col-end-9": colEnd === 9,
          "lg:col-end-10": colEnd === 10,
          "lg:col-end-11": colEnd === 11,
          "lg:col-end-12": colEnd === 12,

          "md:col-end-1": mdColEnd === 1,
          "md:col-end-2": mdColEnd === 2,
          "md:col-end-3": mdColEnd === 3,
          "md:col-end-4": mdColEnd === 4,
          "md:col-end-5": mdColEnd === 5,
          "md:col-end-6": mdColEnd === 6,
          "md:col-end-7": mdColEnd === 7,
          "md:col-end-8": mdColEnd === 8,
          "md:col-end-9": mdColEnd === 9,
          "md:col-end-10": mdColEnd === 10,
          "md:col-end-11": mdColEnd === 11,
          "md:col-end-12": mdColEnd === 12,

          "lg:row-start-1": rowStart === 1,
          "lg:row-start-2": rowStart === 2,
          "lg:row-start-3": rowStart === 3,
          "lg:row-start-4": rowStart === 4,
          "lg:row-start-5": rowStart === 5,
          "lg:row-start-6": rowStart === 6,
          "lg:row-start-7": rowStart === 7,
          "lg:row-start-8": rowStart === 8,
          "lg:row-start-9": rowStart === 9,
          "lg:row-start-10": rowStart === 10,
          "lg:row-start-11": rowStart === 11,
          "lg:row-start-12": rowStart === 12,

          "md:row-start-1": mdRowStart === 1,
          "md:row-start-2": mdRowStart === 2,
          "md:row-start-3": mdRowStart === 3,
          "md:row-start-4": mdRowStart === 4,
          "md:row-start-5": mdRowStart === 5,
          "md:row-start-6": mdRowStart === 6,
          "md:row-start-7": mdRowStart === 7,
          "md:row-start-8": mdRowStart === 8,
          "md:row-start-9": mdRowStart === 9,
          "md:row-start-10": mdRowStart === 10,
          "md:row-start-11": mdRowStart === 11,
          "md:row-start-12": mdRowStart === 12,

          "lg:row-end-1": rowEnd === 1,
          "lg:row-end-2": rowEnd === 2,
          "lg:row-end-3": rowEnd === 3,
          "lg:row-end-4": rowEnd === 4,
          "lg:row-end-5": rowEnd === 5,
          "lg:row-end-6": rowEnd === 6,
          "lg:row-end-7": rowEnd === 7,
          "lg:row-end-8": rowEnd === 8,
          "lg:row-end-9": rowEnd === 9,
          "lg:row-end-10": rowEnd === 10,
          "lg:row-end-11": rowEnd === 11,
          "lg:row-end-12": rowEnd === 12,

          "md:row-end-1": mdRowEnd === 1,
          "md:row-end-2": mdRowEnd === 2,
          "md:row-end-3": mdRowEnd === 3,
          "md:row-end-4": mdRowEnd === 4,
          "md:row-end-5": mdRowEnd === 5,
          "md:row-end-6": mdRowEnd === 6,
          "md:row-end-7": mdRowEnd === 7,
          "md:row-end-8": mdRowEnd === 8,
          "md:row-end-9": mdRowEnd === 9,
          "md:row-end-10": mdRowEnd === 10,
          "md:row-end-11": mdRowEnd === 11,
          "md:row-end-12": mdRowEnd === 12,
        },
        className
      )}
    >
      {children}
    </div>
  );
};
