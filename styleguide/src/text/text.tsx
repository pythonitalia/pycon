import clsx from "clsx";
import React from "react";

type Props = React.PropsWithChildren<{
  size?: 1 | 2 | 3 | "label1" | "label2" | "label3" | "label4";
  weight?: "regular" | "strong";
  as?: "span" | "p";
  className?: string;
  color?: "default" | "none";
}>;

export const Text = React.forwardRef<any, Props>(
  (
    {
      children,
      as: As = "span",
      size = 1,
      weight = "regular",
      className = "",
      color = "default",
    },
    ref
  ) => {
    return (
      <As
        className={clsx(
          "font-sans whitespace-pre-wrap",
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
            "text-black": color === "default",
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
