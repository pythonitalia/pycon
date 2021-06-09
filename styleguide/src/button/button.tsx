import clsx from "clsx";
import React, { ReactNode } from "react";
import { Color } from "../types";

export const Button = ({
  children,
  onClick,
  color = "white",
}: {
  color?: Color;
  children: ReactNode;
  onClick: () => void;
}) => (
  <button
    className={clsx("border-black border-2 p-3", {
      "bg-aquamarine": color === "aquamarine",
      "bg-casablanca": color === "casablanca",
      "bg-orange": color === "orange",
      "bg-keppel": color === "casablanca",
      "bg-pink": color === "pink",
      "bg-purple": color === "purple",
      "bg-white": color === "white",
      "bg-black": color === "black",
      "text-white": color === "black",
    })}
    onClick={onClick}
  >
    {children}
  </button>
);
