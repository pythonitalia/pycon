import clsx from "clsx";
import React, { ReactNode } from "react";
import { Color } from "../types";

export const Paragraph = ({
  children,
  bold = false,
  color = "black",
}: {
  children: ReactNode;
  bold?: boolean;
  color?: Color;
}) => (
  <p
    className={clsx("mb-8", {
      "font-bold": bold,
      "text-blue": color === "blue",
      "text-coral": color === "coral",
      "text-black": color === "black",
      "text-green": color === "green",
      "text-pink": color === "pink",
      "text-purple": color === "purple",
      "text-white": color === "white",
    })}
  >
    {children}
  </p>
);
