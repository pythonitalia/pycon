import clsx from "clsx";
import React from "react";
import {
  getStyleClassesHoverTextColor,
  getStyleClassesTextColor,
} from "../colors-utils";
import { Color } from "../types";

type Props = {
  children: React.ReactNode;
  size?: 1 | 2 | 3 | "label1" | "label2" | "label3" | "label4" | "inherit";
  weight?: "regular" | "strong";
  align?: "left" | "center" | "right";
  as?: "span" | "p";
  className?: string;
  color?: Color | "none" | "default";
  hoverColor?: Color | "none" | "default";
  noWrap?: boolean;
  uppercase?: boolean;
  decoration?: "none" | "underline" | "line-through";
  onClick?: () => void;
  select?: "none" | "auto";
};

export const getStyleClassesForTextSize = (size: Props["size"]) => {
  switch (size) {
    case 1:
      return "text-md leading-7 lg:text-2md lg:leading-8";
    case 2:
      return "text-md leading-7";
    case 3:
      return "text-base leading-4";
    case "label1":
      return "text-base leading-1 lg:text-2md lg:leading-4";
    case "label2":
      return "text-base leading-1 lg:text-md lg:leading-2";
    case "label3":
      return "text-base leading-1";
    case "label4":
      return "text-sm leading-0.5";
    case "inherit":
    default:
      return "";
  }
};

export const Text = React.forwardRef<any, Props>(
  (
    {
      children,
      as: As = "span",
      size = 1,
      weight = "regular",
      className = "",
      color = "default",
      hoverColor = "none",
      noWrap = false,
      uppercase = false,
      decoration = "none",
      align,
      onClick,
      select = "auto",
    },
    ref
  ) => {
    return (
      <As
        className={clsx(
          "font-sans break-words transition-colors",
          {
            "font-medium": weight === "regular",
            "font-semibold": weight === "strong",

            underline: decoration === "underline",
            "line-through": decoration === "line-through",

            "whitespace-nowrap": noWrap,
            "whitespace-pre-wrap": !noWrap,

            uppercase: uppercase,

            "text-left": align === "left",
            "text-center": align === "center",
            "text-right": align === "right",

            "cursor-pointer": !!onClick,

            "select-none": select === "none",
            "select-auto": select === "auto",
          },
          getStyleClassesForTextSize(size),
          getStyleClassesTextColor(color),
          getStyleClassesHoverTextColor(hoverColor),
          className
        )}
        ref={ref}
        onClick={onClick}
      >
        {children}
      </As>
    );
  }
);
