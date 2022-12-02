import clsx from "clsx";
import React, { ReactNode } from "react";

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
}: {
  children: ReactNode;
  size?: Size;
}) => {
  const Component = SIZE_TO_COMPONENT[size];
  return (
    <Component
      className={clsx("text-black font-semibold", {
        "text-2xl leading-12 sm:text-4xl sm:leading-15": size === "display1",
        "text-2lg leading-9 sm:text-3xl sm:leading-14": size === "display2",
        "text-2lg leading-10 sm:text-2xl sm:leading-13": size === 1,
        "text-3md leading-8 sm:text-xl sm:leading-11": size === 2,
        "text-2md leading-5 sm:text-lg sm:leading-8": size === 3,
        "text-md  leading-3 sm:text-2md sm:leading-6": size === 4,
        "text-base leading-2 sm:text-md sm:leading-4": size === 5,
        "text-sm leading-1 sm:text-base sm:leading-2": size === 6,
      })}
    >
      {children}
    </Component>
  );
};
