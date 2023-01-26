import clsx from "clsx";
import React from "react";
import { getBackgroundClasses } from "../colors-utils";
import { Color } from "../types";

type Props = {
  children: React.ReactNode;
  as?: React.ElementType<{
    className?: string;
  }>;
  position?: "absolute" | "relative" | "fixed" | "static" | "sticky";
  bottom?: number;
  background?: Color | "none";
  zIndex?: 0 | 1 | 10;
  style?: React.CSSProperties;
  fullScreenHeight?: boolean;
  overflow?: "scroll" | "auto" | "hidden" | "visible";
  showFrom?: "mobile" | "tablet" | "desktop";
  showUntil?: "tablet" | "desktop";
};
export const LayoutContent = ({
  children,
  fullScreenHeight,
  overflow,
  showFrom,
  showUntil,
  position,
  style,
  zIndex,
  background = "none",
  as: Component = "div",
}: Props) => {
  return (
    <Component
      className={clsx({
        ...getBackgroundClasses(background),

        "hidden lg:block": showFrom === "desktop",
        "hidden md:block": showFrom === "tablet",

        "block lg:hidden": showUntil === "desktop",
        "block md:hidden": showUntil === "tablet",

        relative: position === "relative",
        absolute: position === "absolute",
        fixed: position === "fixed",
        static: position === "static",
        sticky: position === "sticky",

        "z-0": zIndex === 0,
        "z-[1]": zIndex === 1,
        "z-10": zIndex === 10,

        "lg:h-screen": fullScreenHeight,

        "lg:overflow-auto": overflow === "auto",
        "lg:overflow-hidden": overflow === "hidden",
        "lg:overflow-scroll": overflow === "scroll",
        "lg:overflow-visible": overflow === "visible",
      })}
      style={style}
    >
      {children}
    </Component>
  );
};
