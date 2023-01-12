import clsx from "clsx";
import React from "react";

type Props = {
  children: React.ReactNode;
  as?: React.ElementType<{
    className?: string;
  }>;
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
  as: Component = "div",
}: Props) => {
  return (
    <Component
      className={clsx({
        "hidden lg:block": showFrom === "desktop",
        "hidden md:block": showFrom === "tablet",

        "block lg:hidden": showUntil === "desktop",
        "block md:hidden": showUntil === "tablet",

        "lg:h-screen": fullScreenHeight,

        "lg:overflow-auto": overflow === "auto",
        "lg:overflow-hidden": overflow === "hidden",
        "lg:overflow-scroll": overflow === "scroll",
        "lg:overflow-visible": overflow === "visible",
      })}
    >
      {children}
    </Component>
  );
};
