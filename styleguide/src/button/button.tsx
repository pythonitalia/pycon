import clsx from "clsx";
import React, { ReactNode } from "react";
import { Color } from "../types";

export const Button = ({
  children,
  onClick,
  icon = null,
  color = "white",
}: {
  color?: Color;
  icon?: ReactNode;
  children: ReactNode;
  onClick: () => void;
}) => (
  <button
    className={clsx(
      "flex items-center justify-items-center border-black border-2 p-3",
      {
        "bg-aquamarine": color === "aquamarine",
        "bg-casablanca": color === "casablanca",
        "bg-orange": color === "orange",
        "bg-keppel": color === "casablanca",
        "bg-pink": color === "pink",
        "bg-purple": color === "purple",
        "bg-white": color === "white",
        "bg-black": color === "black",
        "text-white": color === "black",
      }
    )}
    onClick={onClick}
  >
    {icon && <span className="mr-2">{icon}</span>}
    {children}
  </button>
);
