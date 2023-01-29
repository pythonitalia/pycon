import clsx from "clsx";
import React from "react";
import { getTextColorClasses } from "../colors-utils";
import { Color } from "../types";

type Props = {
  children: React.ReactNode;
  size?: 1 | 2 | 3 | "label1" | "label2" | "label3" | "label4" | "inherit";
  weight?: "regular" | "strong";
  align?: "left" | "center" | "right";
  as?: "span" | "p";
  className?: string;
  color?: Color | "none" | "default";
  noWrap?: boolean;
  uppercase?: boolean;
  decoration?: "none" | "underline" | "line-through";
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
      noWrap = false,
      uppercase = false,
      decoration = "none",
      align,
    },
    ref
  ) => {
    return (
      <As
        className={clsx(
          "font-sans break-words",
          {
            "text-md leading-7 lg:text-2md lg:leading-8": size === 1,
            "text-md leading-7": size === 2,
            "text-base leading-4": size === 3,
            "24px text-2md leading-4": size === "label1",
            "20px text-md leading-2": size === "label2",
            "16px text-base leading-1": size === "label3",
            "14px text-sm leading-0.5 ": size === "label4",

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

            ...getTextColorClasses(color),
          },
          className
        )}
        ref={ref}
      >
        {children}
      </As>
    );
  }
);
