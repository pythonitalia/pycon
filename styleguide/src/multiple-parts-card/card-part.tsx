import React from "react";
import { Heading } from "../heading";
import { Spacer } from "../spacer";
import clsx from "clsx";

type CardPartProps = React.PropsWithChildren<{
  title?: string | React.ReactNode;
  titleSize?: "default" | "small" | "large";
  noBg?: boolean;
  contentAlign?: "right" | "left" | "center";
}>;

export const CardPart = ({
  title,
  children,
  titleSize = "default",
  noBg = false,
  contentAlign = "center",
}: CardPartProps) => {
  return (
    <div
      className={clsx("p-4 lg:p-6", {
        "bg-milk": noBg,
        "bg-cream": !noBg,

        "text-right": contentAlign === "right",
        "text-left": contentAlign === "left",
        "text-center": contentAlign === "center",
      })}
    >
      {title && (
        <>
          <Heading size={getTitleSize(titleSize)}>{title}</Heading>
          {children && <Spacer size="xs" />}
        </>
      )}

      {children}
    </div>
  );
};

const getTitleSize = (value: CardPartProps["titleSize"]) => {
  switch (value) {
    case "small":
      return 3;
    case "large":
      return 1;
    case "default":
    default:
      return 2;
  }
};
