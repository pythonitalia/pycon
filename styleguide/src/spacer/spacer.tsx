import clsx from "clsx";
import React from "react";

type Breakpoint = "mobile" | "tablet" | "desktop";

type Props = {
  size:
    | "none"
    | "thin"
    | "xs"
    | "small"
    | "medium"
    | "2md"
    | "large"
    | "xl"
    | "2xl"
    | "3xl";
  showOnlyOn?: Breakpoint;
  orientation?: "horizontal" | "vertical";
};

export const Spacer = ({
  size,
  orientation = "vertical",
  showOnlyOn,
}: Props) => {
  if (size === "none") {
    return null;
  }

  return (
    <span
      className={clsx({
        // vertical spacers
        "h-[2px]": size === "thin" && orientation === "vertical",
        "h-2": size === "xs" && orientation === "vertical",
        "h-2 lg:h-4": size === "small" && orientation === "vertical",
        "h-6": size === "medium" && orientation === "vertical",
        "h-5 lg:h-8": size === "2md" && orientation === "vertical",
        "h-8 lg:h-12": size === "large" && orientation === "vertical",
        "h-12 lg:h-16": size === "xl" && orientation === "vertical",
        "h-12 lg:h-20": size === "2xl" && orientation === "vertical",
        "h-16 lg:h-32": size === "3xl" && orientation === "vertical",

        // horizontal spacers
        "w-12": size == "large" && orientation === "horizontal",
        "w-2 lg:w-4": size == "small" && orientation === "horizontal",
        "w-2": size == "xs" && orientation === "horizontal",

        block: !showOnlyOn && orientation === "vertical",
        "inline-block": !showOnlyOn && orientation === "horizontal",

        // displays
        "block md:hidden":
          showOnlyOn === "mobile" && orientation === "vertical",
        "inline-block md:hidden":
          showOnlyOn === "mobile" && orientation === "horizontal",

        "hidden md:block lg:hidden":
          showOnlyOn === "tablet" && orientation === "vertical",
        "hidden md:inline-block lg:hidden":
          showOnlyOn === "tablet" && orientation === "horizontal",

        "hidden md:hidden lg:block":
          showOnlyOn === "desktop" && orientation === "vertical",
        "hidden md:hidden lg:inline-block":
          showOnlyOn === "desktop" && orientation === "horizontal",
      })}
    />
  );
};
