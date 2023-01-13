import clsx from "clsx";
import React, { ReactNode } from "react";
import { getTextColorClasses } from "../colors-utils";
import { Color } from "../types";

type Size = "display1" | "display2" | 1 | 2 | 3 | 4 | 5 | 6;

const SIZE_TO_COMPONENT: { [size in Size]: React.ElementType } = {
  display1: "h1",
  display2: "h1",
  1: "h1",
  2: "h2",
  3: "h3",
  4: "h4",
  5: "h5",
  6: "h6",
};

export const Heading = ({
  children,
  size = 1,
  color = "black",
  align,
  className,
  uppercase = false,
}: {
  children: ReactNode;
  size?: Size;
  color?: Color | "none";
  align?: "left" | "center" | "right";
  className?: string;
  uppercase?: boolean;
}) => {
  const Component = SIZE_TO_COMPONENT[size];
  return (
    <Component
      className={clsx(
        "font-sans",
        {
          "font-bold text-2xl leading-12 lg:text-4xl lg:leading-15":
            size === "display1",
          "font-bold text-2lg leading-9 lg:text-3xl lg:leading-14":
            size === "display2",
          "font-semibold text-2lg leading-10 lg:text-2xl lg:leading-13":
            size === 1,
          "font-semibold text-3md leading-8 lg:text-xl lg:leading-11":
            size === 2,
          "font-semibold text-2md leading-5 lg:text-lg lg:leading-8":
            size === 3,
          "font-semibold text-md  leading-3 lg:text-2md lg:leading-6":
            size === 4,
          "font-semibold text-base leading-2 lg:text-md lg:leading-4":
            size === 5,
          "font-semibold text-sm leading-1 lg:text-base lg:leading-2":
            size === 6,

          uppercase: uppercase,

          "text-left": align === "left",
          "text-center": align === "center",
          "text-right": align === "right",

          ...getTextColorClasses(color),
        },
        className
      )}
    >
      {children}
    </Component>
  );
};
