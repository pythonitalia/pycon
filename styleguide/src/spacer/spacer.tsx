import clsx from "clsx";
import React from "react";

type Breakpoint = "mobile" | "tablet" | "desktop";

type Props = {
  size: "xs" | "small" | "medium" | "2md" | "large" | "xl";
  showOnlyOn?: Breakpoint;
  orientation?: "horizontal" | "vertical";
};

export const Spacer = ({
  size,
  orientation = "vertical",
  showOnlyOn,
}: Props) => {
  return (
    <span
      className={clsx({
        // vertical spacers
        "h-2": size === "xs" && orientation === "vertical",
        "h-4": size === "small" && orientation === "vertical",
        "h-6": size === "medium" && orientation === "vertical",
        "h-5 lg:h-8": size === "2md" && orientation === "vertical",
        "h-8 lg:h-12": size === "large" && orientation === "vertical",
        "h-12 lg:h-16": size === "xl" && orientation === "vertical",

        // horizontal spacers
        "w-12": size == "large" && orientation === "horizontal",

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
