import clsx from "clsx";
import React, { ReactNode } from "react";

type Props = {
  children: ReactNode;
  align?: "left" | "center" | "right";
  gap?: "none" | "xs" | "small";
};

export const HorizontalStack = ({ children, gap = "none", align }: Props) => (
  <div
    className={clsx("flex flex-row", {
      "items-start justify-content-start": align === "left",
      "items-center justify-content-center": align === "center",
      "items-end justify-content-end": align === "right",

      "gap-0": gap === "none",
      "gap-1": gap === "xs",
      "gap-2": gap === "small",
    })}
  >
    {children}
  </div>
);
