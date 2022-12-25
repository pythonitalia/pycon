import clsx from "clsx";
import React from "react";
import { Text } from "../text";
import { Color } from "../types";

type Props = {
  size?: "small" | "big";
  children: React.ReactNode;
  color: Color;
};

export const Tag = ({ children, size = "big", color }: Props) => {
  return (
    <div
      className={clsx(
        "flex items-center justify-center border border-black py-2 px-4 select-none",
        {
          "bg-coral text-black": color === "coral",
          "bg-caramel text-black": color === "caramel",
          "bg-cream text-black": color === "cream",
          "bg-yellow text-black": color === "yellow",
          "bg-green text-black": color === "green",
          "bg-purple text-black": color === "purple",
          "bg-pink text-black": color === "pink",
          "bg-blue text-black": color === "blue",
          "bg-red text-black": color === "red",
          "bg-success text-black": color === "success",
          "bg-warning text-black": color === "warning",
          "bg-neutral text-black": color === "neutral",
          "bg-black text-white": color === "black",
          "bg-grey-250 text-black": color === "grey",
          "bg-white text-black": color === "white",
          "bg-milk text-black": color === "milk",
        }
      )}
    >
      <Text
        color="none"
        weight="strong"
        uppercase
        size={size === "big" ? "label3" : "label4"}
      >
        {children}
      </Text>
    </div>
  );
};
