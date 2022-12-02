import clsx from "clsx";
import React from "react";

type Props = React.PropsWithChildren<{
  size?: 1 | 2 | 3;
  weight?: "regular" | "strong";
  as?: "span" | "p";
}>;

export const Text = ({
  children,
  as: As = "span",
  size = 1,
  weight = "regular",
}: Props) => {
  return (
    <As
      className={clsx("text-black", {
        "text-md leading-7 sm:text-2md sm:leading-8": size === 1,
        "text-md leading-7": size === 2,
        "text-base leading-4": size === 3,
        "font-medium": weight === "regular",
        "font-semibold": weight === "strong",
      })}
    >
      {children}
    </As>
  );
};
